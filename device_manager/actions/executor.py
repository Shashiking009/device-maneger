import time
import threading
from typing import Dict, Any, Tuple, Optional
from actions.models import ActionPlan, Action, ActionType, ActionStatus
from capabilities.capability_registry import capability_registry
from events import event_bus, SpidyEvent

class ActionExecutor:
    """
    Action Plan Execution Subsystem.
    Executes sequential/multi-step action plans through CapabilityRegistry.
    Handles step-by-step execution, failure rollbacks, and progress event publishing.
    """
    def __init__(self):
        self.active_plan: Optional[ActionPlan] = None
        self._lock = threading.Lock()

    def execute_plan(self, plan: ActionPlan, dry_run: bool = False) -> ActionPlan:
        if dry_run:
            plan.status = ActionStatus.COMPLETED
            for a in plan.actions:
                a.status = ActionStatus.COMPLETED
                a.message = "Dry-run execution simulated."
            return plan
        if not self._lock.acquire(blocking=False):
            plan.status = ActionStatus.FAILED
            event_bus.publish(SpidyEvent(
                event_type="ACTION_PLAN_FAILED",
                state="ERROR",
                message="Another action plan is currently executing."
            ))
            return plan

        try:
            self.active_plan = plan
            plan.status = ActionStatus.EXECUTING
            
            event_bus.publish(SpidyEvent(
                event_type="ACTION_PLAN_STARTED",
                state="EXECUTING",
                message=f"Executing plan '{plan.plan_id}' with {len(plan.actions)} steps."
            ))

            for idx, action in enumerate(plan.actions):
                action.status = ActionStatus.EXECUTING
                event_bus.publish(SpidyEvent(
                    event_type="ACTION_STEP_STARTED",
                    state="EXECUTING",
                    message=f"Step {idx+1}/{len(plan.actions)}: {action.action_type.value}"
                ))

                success, msg = self._execute_single_action(action)
                action.message = msg

                if success:
                    action.status = ActionStatus.COMPLETED
                    event_bus.publish(SpidyEvent(
                        event_type="ACTION_STEP_COMPLETED",
                        state="EXECUTING",
                        message=f"Step {idx+1} completed: {msg}"
                    ))
                else:
                    action.status = ActionStatus.FAILED
                    plan.status = ActionStatus.FAILED
                    event_bus.publish(SpidyEvent(
                        event_type="ACTION_STEP_FAILED",
                        state="ERROR",
                        message=f"Step {idx+1} failed: {msg}"
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
            return capability_registry.apps.launch_application(app)

        elif t == ActionType.CLOSE_APPLICATION:
            app = p.get("application", "")
            resp = capability_registry.apps.close_application(app)
            return resp.success, resp.message

        elif t == ActionType.OPEN_FOLDER:
            folder = p.get("folder", "")
            resp = capability_registry.files.open_folder(folder)
            return resp.success, resp.message

        elif t == ActionType.TYPE_TEXT:
            text = p.get("text", "")
            resp = capability_registry.keyboard.type_text(text)
            return resp.success, resp.message

        elif t == ActionType.VOLUME_UP:
            resp = capability_registry.system.set_volume("up")
            return resp.success, resp.message

        elif t == ActionType.VOLUME_DOWN:
            resp = capability_registry.system.set_volume("down")
            return resp.success, resp.message

        return False, f"Unsupported action type: {t}"

action_executor = ActionExecutor()
