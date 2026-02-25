from typing import Any, Dict, List


class ConversationState:
    """
    Minimal state holder for the clarification loop.
    Tracks history and missing fields from the model output.
    """

    def __init__(self) -> None:
        self.history: List[Dict[str, Any]] = []
        self.missing_fields: List[str] = []

    def update(self, data: Dict[str, Any]) -> None:
        self.missing_fields = data.get("missing_fields", [])
        self.history.append(data)

    def needs_clarification(self) -> bool:
        return len(self.missing_fields) > 0

