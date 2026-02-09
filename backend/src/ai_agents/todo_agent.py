"""
AI Agent for Todo Application

This agent uses OpenAI's API to understand natural language requests
and interacts with the system through MCP tools.
"""
import os
from typing import Dict, Any, List
from openai import OpenAI
from mcp_server.tools.list_tasks import list_tasks, ListTasksArgs
from mcp_server.tools.create_task import create_task_tool, CreateTaskArgs
from mcp_server.tools.get_task import get_task, GetTaskArgs
from mcp_server.tools.update_task import update_task_tool, UpdateTaskArgs
from mcp_server.tools.delete_task import delete_task_tool, DeleteTaskArgs
from mcp_server.tools.toggle_task import toggle_task, ToggleTaskArgs


class TodoAgent:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-3.5-turbo"
        else:
            # Create a mock client for development when API key is not available
            self.client = None
            self.model = None
    
    async def process_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response.

        Args:
            user_id: The ID of the user sending the message
            message: The natural language message from the user

        Returns:
            Dictionary containing the agent's response and any tool calls made
        """
        # If no OpenAI client is available, return a helpful message
        if not self.client or not self.model:
            return {
                "response": "AI agent is not configured. Please set the OPENAI_API_KEY environment variable to enable AI features.",
                "tool_calls": [],
                "timestamp": 0
            }
        
        # Define the system prompt to constrain the agent's behavior
        system_prompt = """
        You are a helpful assistant for managing todo tasks. You can help users create,
        read, update, and delete tasks. You can also mark tasks as complete or incomplete.

        You must use the provided tools to interact with the task system.
        You are NOT allowed to access the database directly.

        Available tools:
        1. list_tasks: Get all tasks for the user
        2. create_task: Create a new task
        3. get_task: Get details of a specific task
        4. update_task: Update an existing task
        5. delete_task: Delete a task
        6. toggle_task: Mark a task as complete/incomplete

        Always be helpful and confirm actions taken.
        """

        # Prepare the conversation history for the API call
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        # Define the tools available to the model
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Get all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "completed": {"type": "boolean", "description": "Filter by completion status"},
                            "limit": {"type": "integer", "description": "Max number of tasks to return"},
                            "offset": {"type": "integer", "description": "Offset for pagination"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "title": {"type": "string", "description": "The task title"},
                            "description": {"type": "string", "description": "The task description"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_task",
                    "description": "Get details of a specific task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The task ID"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The task ID"},
                            "title": {"type": "string", "description": "The new task title"},
                            "description": {"type": "string", "description": "The new task description"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The task ID"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "toggle_task",
                    "description": "Mark a task as complete/incomplete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "task_id": {"type": "string", "description": "The task ID"},
                            "completed": {"type": "boolean", "description": "Whether the task is completed"}
                        },
                        "required": ["user_id", "task_id", "completed"]
                    }
                }
            }
        ]

        # Call the OpenAI API with function calling
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
        except Exception as e:
            # Return a helpful error message if OpenAI API is not properly configured
            return {
                "response": "I'm having trouble connecting to my brain right now. Please make sure the OpenAI API key is properly configured.",
                "tool_calls": [],
                "timestamp": 0
            }
        
        # Process the response
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        tool_results = []
        ai_response = ""
        
        if tool_calls:
            # Execute the requested tools
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                try:
                    # Safely evaluate the arguments
                    import json
                    function_args = json.loads(tool_call.function.arguments)
                except:
                    # If JSON parsing fails, try eval as fallback
                    function_args = eval(tool_call.function.arguments)
                
                # Add user_id to the arguments if not present
                if "user_id" not in function_args:
                    function_args["user_id"] = user_id
                
                # Execute the appropriate tool
                try:
                    if function_name == "list_tasks":
                        args = ListTasksArgs(**function_args)
                        result = await list_tasks(args)
                    elif function_name == "create_task":
                        args = CreateTaskArgs(**function_args)
                        result = await create_task_tool(args)
                    elif function_name == "get_task":
                        args = GetTaskArgs(**function_args)
                        result = await get_task(args)
                    elif function_name == "update_task":
                        args = UpdateTaskArgs(**function_args)
                        result = await update_task_tool(args)
                    elif function_name == "delete_task":
                        args = DeleteTaskArgs(**function_args)
                        result = await delete_task_tool(args)
                    elif function_name == "toggle_task":
                        args = ToggleTaskArgs(**function_args)
                        result = await toggle_task(args)
                    else:
                        result = {"error": f"Unknown tool: {function_name}"}
                    
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "result": result
                    })
                except Exception as e:
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "result": {"error": str(e)}
                    })
            
            # If there were tool calls, get a final response from the model
            # incorporating the tool results
            follow_up_messages = messages + [
                response_message,
            ]
            
            for tool_result in tool_results:
                follow_up_messages.append({
                    "role": "tool",
                    "content": str(tool_result["result"]),
                    "tool_call_id": tool_result["tool_call_id"]
                })
            
            # Get the final response from the model
            try:
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=follow_up_messages
                )
                
                ai_response = final_response.choices[0].message.content
            except Exception as e:
                ai_response = "I processed your request but am having trouble formulating a response."
        else:
            # If no tools were called, use the initial response
            ai_response = response_message.content
        
        return {
            "response": ai_response,
            "tool_calls": [
                {
                    "tool_name": tc.function.name,
                    "arguments": eval(tc.function.arguments) if tc.function.arguments else {},
                    "result": next((tr["result"] for tr in tool_results if tr["tool_call_id"] == tc.id), {})
                }
                for tc in tool_calls
            ] if tool_calls else [],
            "timestamp": getattr(response, 'created', 0)
        }