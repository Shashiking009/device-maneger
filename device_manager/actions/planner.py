import re
from typing import List, Dict, Any, Optional
from actions.models import Action, ActionPlan, ActionType, RiskLevel, ActionStatus
from actions.validator import validator
from actions.config import MAX_PLAN_STEPS, ALLOWED_APPLICATIONS

class ActionPlanner:
    """
    Intelligent Action Planner.
    Deconstructs multi-intent natural language requests into structured, validated ActionPlans.
    """
    def create_plan(self, query: str) -> ActionPlan:
        clean_query = query.strip().lower()
        
        # Remove wake word prefixes if present
        clean_query = re.sub(r"^(hey|hi|ok)\s+spidy[,:]?\s*", "", clean_query)

        actions: List[Action] = []
        
        # Split multi-step conjunctions ("and then", "and", "then", ",")
        parts = [p.strip() for p in re.split(r"\b(and then|and|then)\b|,", clean_query) if p and p not in ["and then", "and", "then", ","]]
        if not parts:
            parts = [clean_query]

        for part in parts[:MAX_PLAN_STEPS]:
            action_item = self._parse_part_to_action(part)
            if action_item:
                valid, msg, risk = validator.validate_action(action_item)
                action_item.risk_level = risk
                if not valid:
                    action_item.status = ActionStatus.REJECTED
                    action_item.error = msg
                else:
                    action_item.status = ActionStatus.VALIDATED
                actions.append(action_item)

        requires_conf = any(a.risk_level in [RiskLevel.HIGH] for a in actions)
        
        plan = ActionPlan(
            original_query=query,
            actions=actions,
            requires_confirmation=requires_conf
        )
        return plan

    def _parse_part_to_action(self, part: str) -> Optional[Action]:
        clean_part = part.strip()

        # Open Application
        open_match = re.search(r"\b(open|launch|start)\s+([a-z0-9\s]+)", clean_part)
        if open_match:
            app_name = open_match.group(2).strip()
            # Remove filler words
            app_name = re.sub(r"\b(app|application|the)\b", "", app_name).strip()
            return Action(action_type=ActionType.OPEN_APPLICATION, parameters={"application": app_name})

        # Check if clean_part itself is in ALLOWED_APPLICATIONS
        if clean_part.lower() in ALLOWED_APPLICATIONS:
            return Action(action_type=ActionType.OPEN_APPLICATION, parameters={"application": clean_part.lower()})

        # Close Application
        close_match = re.search(r"\b(close|quit|exit|stop)\s+([a-z0-9\s]+)", part)
        if close_match and "spidy" not in part:
            app_name = close_match.group(2).strip()
            app_name = re.sub(r"\b(app|application|the)\b", "", app_name).strip()
            return Action(action_type=ActionType.CLOSE_APPLICATION, parameters={"application": app_name})

        # Type Text
        type_match = re.search(r"\b(type|write)\s+(.+)", part)
        if type_match:
            text = type_match.group(2).strip()
            return Action(action_type=ActionType.TYPE_TEXT, parameters={"text": text})

        # Volume
        if "volume up" in part or "increase volume" in part:
            return Action(action_type=ActionType.VOLUME_UP)
        elif "volume down" in part or "decrease volume" in part:
            return Action(action_type=ActionType.VOLUME_DOWN)
        elif "mute" in part:
            return Action(action_type=ActionType.MUTE)
        elif "unmute" in part:
            return Action(action_type=ActionType.UNMUTE)

        # Lock Screen
        if "lock screen" in part or "lock computer" in part:
            return Action(action_type=ActionType.LOCK_SCREEN)

        return None

planner = ActionPlanner()
