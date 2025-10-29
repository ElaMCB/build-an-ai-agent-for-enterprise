"""Agent orchestrator implementing ReAct pattern."""

from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool
from src.utils.llm_config import get_chat_llm
from typing import Dict, Any
import os


class AgentOrchestrator:
    """Main agent orchestrator using ReAct pattern."""
    
    def __init__(self, rag_tool, ticket_tool):
        self.rag_tool = rag_tool
        self.ticket_tool = ticket_tool
        self.agent = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the ReAct agent with tools."""
        # Define tools
        tools = [
            StructuredTool.from_function(
                func=self._query_policies,
                name="policy_query",
                description=self.rag_tool.get_tool_description()
            ),
            StructuredTool.from_function(
                func=self._create_ticket,
                name="create_ticket",
                description=self.ticket_tool.get_tool_description()
            )
        ]
        
        # Create prompt template
        prompt = PromptTemplate.from_template("""
You are a helpful AI assistant for an enterprise organization. Your role is to help employees with:
1. Answering questions about company policies using the policy_query tool
2. Creating helpdesk tickets for IT requests, equipment needs, and access requests using the create_ticket tool

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Available tools:
{tools}

Use the following guidelines:
- For policy questions, use policy_query to search the knowledge base
- For requests to create tickets, file requests, or take actions, use create_ticket
- If the user's intent is unclear, ask for clarification
- Be professional and helpful

Question: {input}
Thought: {agent_scratchpad}
""")
        
        # Initialize LLM (supports OpenAI or DeepSeek)
        llm = get_chat_llm(model="gpt-4o-mini", temperature=0)
        
        # Create agent
        agent = create_react_agent(llm, tools, prompt)
        
        # Create agent executor
        self.agent = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def _query_policies(self, question: str) -> str:
        """Wrapper for RAG tool query."""
        try:
            result = self.rag_tool.query(question)
            return f"Answer: {result['answer']}\nSources: {', '.join(result.get('sources', []))}"
        except Exception as e:
            return f"Error querying policies: {str(e)}"
    
    def _create_ticket(self, subject: str, description: str, priority: str = "medium", category: str = "general") -> str:
        """Wrapper for ticket creation."""
        try:
            ticket = self.ticket_tool.create_ticket(
                subject=subject,
                description=description,
                priority=priority,
                category=category
            )
            return f"Ticket created successfully! Ticket ID: {ticket['id']}, Subject: {ticket['subject']}, Status: {ticket['status']}"
        except Exception as e:
            return f"Error creating ticket: {str(e)}"
    
    def process(self, user_input: str) -> Dict[str, Any]:
        """Process user input and return response."""
        try:
            response = self.agent.invoke({"input": user_input})
            return {
                "response": response.get("output", "I couldn't process that request."),
                "success": True
            }
        except Exception as e:
            return {
                "response": f"An error occurred: {str(e)}",
                "success": False
            }

