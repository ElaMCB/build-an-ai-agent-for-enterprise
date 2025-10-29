"""Ticket creation tool for helpdesk automation."""

from typing import Dict, List
from datetime import datetime
import json
import os


class TicketTool:
    """Tool for creating helpdesk tickets."""
    
    def __init__(self, tickets_file: str = "./data/tickets.json"):
        self.tickets_file = tickets_file
        self._ensure_tickets_file()
    
    def _ensure_tickets_file(self):
        """Ensure tickets file exists."""
        os.makedirs(os.path.dirname(self.tickets_file) if os.path.dirname(self.tickets_file) else ".", exist_ok=True)
        if not os.path.exists(self.tickets_file):
            with open(self.tickets_file, 'w') as f:
                json.dump({"tickets": []}, f)
    
    def create_ticket(self, subject: str, description: str, priority: str = "medium", category: str = "general") -> Dict:
        """Create a helpdesk ticket."""
        # Load existing tickets
        with open(self.tickets_file, 'r') as f:
            data = json.load(f)
        
        # Generate ticket ID
        ticket_id = f"TKT-{len(data['tickets']) + 1:05d}"
        
        # Create ticket
        ticket = {
            "id": ticket_id,
            "subject": subject,
            "description": description,
            "priority": priority.lower(),
            "category": category.lower(),
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save ticket
        data["tickets"].append(ticket)
        with open(self.tickets_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return ticket
    
    def get_ticket(self, ticket_id: str) -> Dict:
        """Get a ticket by ID."""
        with open(self.tickets_file, 'r') as f:
            data = json.load(f)
        
        for ticket in data["tickets"]:
            if ticket["id"] == ticket_id:
                return ticket
        
        return None
    
    def list_tickets(self, limit: int = 10) -> List[Dict]:
        """List recent tickets."""
        with open(self.tickets_file, 'r') as f:
            data = json.load(f)
        
        return data["tickets"][-limit:]
    
    def get_tool_description(self) -> str:
        """Return tool description for agent."""
        return """Use this tool to create helpdesk tickets for:
        - IT equipment requests (laptops, monitors, accessories)
        - Software license requests
        - Access requests (database, servers, applications)
        - Technical support issues
        - Equipment repairs or replacements
        Returns a ticket ID that can be tracked."""
    
    def get_tool_name(self) -> str:
        """Return tool name."""
        return "create_ticket"

