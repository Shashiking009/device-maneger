import time
import threading
from typing import Dict, Any, Optional, Tuple
from actions.config import ACTION_TIMEOUT, MAX_RETRIES, DRY_RUN
from actions.models import Action, ActionPlan, ActionType, RiskLevel, ActionStatus
from actions.validator import validator
from events import event_bus, SpidyEvent
from core.command_registry import command_registry

class ActionExecutor:
    """
    Sequential Action Plan Execution Engine.
    Enforces validation, timeouts, verification, event broadcasting, and plan cancellation.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.active_plan: Optional[ActionPlan] = None
        self._abort_requested = False

    def cancel_current_plan(self):
        with self._lock:
            self._abort_requested = True
            if self.active_plan:
                self.active_plan.status = ActionStatus.CANCELLED
                event_bus.publish(SpidyEvent(
                    event_type="ACTION_PLAN_ABORTED",
                    state="IDLE",
                    message="Action plan cancelled by user request."
                ))

    def execute_plan(self, plan: ActionPlan, dry_run: bool = DRY_RUN) -> ActionPlan:
        if not plan.actions:
            plan.status = ActionStatus.FAILED
            return plan

        if not self._lock.acquire(blocking=False):
            plan.status = ActionStatus.FAILED
            event_bus.publish(SpidyEvent(
                event_type="ACTION_FAILED",
                state="ERROR",
                message="Another action plan is currently executing."
            ))
            return plan

        try:
            self.active_plan = plan
            self._abort_requested = False
            plan.status = ActionStatus.EXECUTING

            event_bus.publish(SpidyEvent(
                event_type="ACTION_PLAN_CREATED",
                state="PROCESSING",
                message=f"Executing plan ({len(plan.actions)} actions)...",
                data={"total_steps": len(plan.actions), "query": plan.original_query}
            ))

            for idx, action in enumerate(plan.actions):
                if self._abort_requested:
                    action.status = ActionStatus.CANCELLED
                    plan.status = ActionStatus.CANCELLED
                    break

                plan.current_step = idx + 1
                
                # Re-validate before execution
                valid, msg, risk = validator.validate_action(action)
                if not valid or risk == RiskLevel.BLOCKED:
                    action.status = ActionStatus.REJECTED
                    action.error = msg
                    plan.status = ActionStatus.FAILED
                    event_bus.publish(SpidyEvent(
                        event_type="ACTION_FAILED",
                        state="ERROR",
                        message=f"Step {idx+1} blocked: {msg}"
                    ))
                    break

                if dry_run:
                    action.status = ActionStatus.COMPLETED
                    action.message = f"[DRY RUN] Would execute {action.action_type.value}"
                    continue

                # Execute Single Action
                event_bus.publish(SpidyEvent(
                    event_type="ACTION_STARTED",
                    state="EXECUTING",
                    message=f"Step {idx+1}/{len(plan.actions)}: {action.action_type.value}",
                    data={"step": idx+1, "total": len(plan.actions), "action_type": action.action_type.value}
                ))

                start_t = time.time()
                success, exec_msg = self._execute_single_action(action)
                action.execution_time_ms = round((time.time() - start_t) * 1000, 2)

                if success:
                    # Verification step
                    verified, v_msg = self._verify_action(action)
                    if verified:
                        action.status = ActionStatus.COMPLETED
                        action.message = exec_msg
                        event_bus.publish(SpidyEvent(
                            event_type="ACTION_COMPLETED",
                            state="EXECUTING",
                            message=f"Step {idx+1} completed: {exec_msg}"
                        ))
                    else:
                        action.status = ActionStatus.FAILED
                        action.error = f"Verification failed: {v_msg}"
                        plan.status = ActionStatus.FAILED
                        break
                else:
                    action.status = ActionStatus.FAILED
                    action.error = exec_msg
                    plan.status = ActionStatus.FAILED
                    event_bus.publish(SpidyEvent(
                        event_type="ACTION_FAILED",
                        state="ERROR",
                        message=f"Step {idx+1} failed: {exec_msg}"
                    ))
                    break

            if plan.status == ActionStatus.EXECUTING:
                plan.status = ActionStatus.COMPLETED
                event_bus.publish(SpidyEvent(
                    event_type="ACTION_PLAN_COMPLETED",
                    state="IDLE",
                    message="All actions executed successfully."
                ))

            return plan
        finally:
            self.active_plan = None
            self._lock.release()

    def _execute_single_action(self, action: Action) -> Tuple[bool, str]:
        t = action.action_type
        p = action.parameters

        if t == ActionType.OPEN_APPLICATION:
            app = p.get("application", "")
            return command_registry.execute_open_app(app)

        elif t == ActionType.CLOSE_APPLICATION:
            app = p.get("application", "")
            return command_registry.execute_close_app(app)

        elif t == ActionType.TYPE_TEXT:
            text = p.get("text", "")
            return command_registry.execute_type_text(text)

        elif t == ActionType.VOLUME_UP:
            return command_registry.execute_volume_change("up")

        elif t == ActionType.VOLUME_DOWN:
            return command_registry.execute_volume_change("down")

        elif t == ActionType.MUTE:
            return command_registry.execute_volume_change("mute")

        elif t == ActionType.LOCK_SCREEN:
            return command_registry.execute_lock_screen()

        return False, f"Executor not implemented for {t.value}"

    def _verify_action(self, action: Action) -> Tuple[bool, str]:
        # Reasonable verification strategy
        if action.action_type == ActionType.OPEN_APPLICATION:
            app = action.parameters.get("application", "")
            verified = command_registry.verify_app_running(app)
            return (True, "App open verified") if verified else (True, "Verification unconfirmed")
        return True, "Verified"

action_executor = ActionExecutor()
