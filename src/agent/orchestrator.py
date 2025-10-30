"""Agent orchestrator with simple intent routing (no AgentExecutor dependency)."""

from typing import Dict, Any


class AgentOrchestrator:
    """Main agent orchestrator using simple heuristics to route intents."""
    
    def __init__(self, rag_tool, ticket_tool):
        self.rag_tool = rag_tool
        self.ticket_tool = ticket_tool

    def _looks_like_ticket_request(self, text: str) -> bool:
        t = text.lower()
        keywords = [
            "ticket", "create ticket", "open ticket", "helpdesk",
            "broken", "replacement", "replace laptop", "repair",
            "software license", "license request", "access request",
            "request access", "database access", "new monitor"
        ]
        return any(k in t for k in keywords)

    def _extract_ticket_fields(self, text: str) -> Dict[str, str]:
        # Very simple extraction; in production, use an LLM or a schema tool
        subject = text.strip()[:120]
        description = text.strip()
        priority = "high" if any(w in text.lower() for w in ["urgent", "critical", "asap"]) else "medium"
        # naive category guess
        if any(w in text.lower() for w in ["laptop", "monitor", "keyboard", "mouse", "hardware", "broken", "replacement"]):
            category = "equipment"
        elif any(w in text.lower() for w in ["license", "software"]):
            category = "software"
        elif "access" in text.lower():
            category = "access"
        else:
            category = "general"
        return {"subject": subject, "description": description, "priority": priority, "category": category}

    def process(self, user_input: str) -> Dict[str, Any]:
        """Process user input and return response."""
        try:
            if self._looks_like_ticket_request(user_input):
                fields = self._extract_ticket_fields(user_input)
                ticket = self.ticket_tool.create_ticket(
                    subject=fields["subject"],
                    description=fields["description"],
                    priority=fields["priority"],
                    category=fields["category"],
                )
                return {
                    "response": f"Ticket created successfully! Ticket ID: {ticket['id']} | Subject: {ticket['subject']} | Status: {ticket['status']}",
                    "success": True,
                }
            # Otherwise query policies via RAG
            result = self.rag_tool.query(user_input)
            answer = result.get("answer", "I couldn't find an answer.")
            sources = ", ".join(result.get("sources", []))
            return {
                "response": f"{answer}\n\nSources: {sources}",
                "success": True,
            }
        except Exception as e:
            return {"response": f"An error occurred: {str(e)}", "success": False}

