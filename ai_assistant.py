"""
AI Assistant module for Personal Assistant
Integrates OpenAI API and LangChain for natural language understanding and responses
"""

import os  # Operating system interface for environment variables
from typing import Dict, List, Optional  # Type hints
from dotenv import load_dotenv  # Load environment variables from .env file
from langchain.llms import OpenAI  # LangChain OpenAI integration
from langchain.chat_models import ChatOpenAI  # LangChain ChatOpenAI integration
from langchain.schema import HumanMessage, SystemMessage  # LangChain message schemas
from langchain.memory import ConversationBufferMemory  # LangChain memory for conversation history
from task_manager import TaskManager  # Import our task manager


class AIAssistant:
    """
    AI Assistant class that handles natural language processing
    and provides intelligent responses using OpenAI and LangChain
    """
    
    def __init__(self, task_manager: TaskManager):
        """
        Initialize the AI Assistant with OpenAI API and LangChain
        
        Args:
            task_manager (TaskManager): Instance of TaskManager for task operations
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Get OpenAI API key from environment
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI Chat model with GPT-3.5-turbo
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model_name="gpt-3.5-turbo",
            temperature=0.7,  # Controls randomness in responses
            max_tokens=500    # Maximum tokens in response
        )
        
        # Initialize conversation memory to maintain context
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Store reference to task manager
        self.task_manager = task_manager
        
        # Define system prompt for the AI assistant
        self.system_prompt = """
        You are a helpful personal assistant that manages daily tasks. 
        Your role is to:
        1. Understand user requests about tasks (creating, viewing, updating, deleting)
        2. Provide helpful and friendly responses
        3. Help users organize their tasks effectively
        4. Give reminders and suggestions when appropriate
        
        You can help with:
        - Creating new tasks from natural language
        - Showing task lists and summaries
        - Marking tasks as complete
        - Deleting tasks
        - Providing task management advice
        
        Always be helpful, concise, and friendly in your responses.
        """
    
    def process_user_input(self, user_input: str) -> Dict:
        """
        Process user input and determine the appropriate action
        
        Args:
            user_input (str): User's natural language input
            
        Returns:
            Dict: Response containing action type, message, and any relevant data
        """
        # Convert input to lowercase for easier processing
        input_lower = user_input.lower()
        
        # Determine the intent of the user's request
        intent = self._classify_intent(input_lower)
        
        # Process based on intent
        if intent == "create_task":
            return self._handle_create_task(user_input)
        elif intent == "view_tasks":
            return self._handle_view_tasks(user_input)
        elif intent == "complete_task":
            return self._handle_complete_task(user_input)
        elif intent == "delete_task":
            return self._handle_delete_task(user_input)
        elif intent == "general_chat":
            return self._handle_general_chat(user_input)
        else:
            return self._handle_unknown_request(user_input)
    
    def _classify_intent(self, user_input: str) -> str:
        """
        Classify user input to determine the intended action
        
        Args:
            user_input (str): User input in lowercase
            
        Returns:
            str: Intent classification (create_task, view_tasks, complete_task, etc.)
        """
        # Keywords for different intents
        create_keywords = ['remind me', 'add', 'create', 'new task', 'schedule', 'set']
        view_keywords = ['show', 'list', 'what', 'tasks', 'todo', 'pending', 'due']
        complete_keywords = ['done', 'complete', 'finished', 'mark as done']
        delete_keywords = ['delete', 'remove', 'cancel', 'drop']
        
        # Check for create task intent
        if any(keyword in user_input for keyword in create_keywords):
            return "create_task"
        
        # Check for view tasks intent
        if any(keyword in user_input for keyword in view_keywords):
            return "view_tasks"
        
        # Check for complete task intent
        if any(keyword in user_input for keyword in complete_keywords):
            return "complete_task"
        
        # Check for delete task intent
        if any(keyword in user_input for keyword in delete_keywords):
            return "delete_task"
        
        # Default to general chat
        return "general_chat"
    
    def _handle_create_task(self, user_input: str) -> Dict:
        """
        Handle task creation requests
        
        Args:
            user_input (str): User's task creation request
            
        Returns:
            Dict: Response with task creation result
        """
        try:
            # Add task using task manager
            task_id = self.task_manager.add_task_from_natural_language(user_input)
            
            # Get the created task details
            task = self.task_manager.db.get_task_by_id(task_id)
            
            # Generate AI response
            ai_response = self._generate_ai_response(
                f"User created a task: {user_input}",
                f"Task created successfully with ID {task_id}"
            )
            
            return {
                'action': 'task_created',
                'message': ai_response,
                'task_id': task_id,
                'task': task if task else None  # Ensure task is not None
            }
            
        except Exception as e:
            return {
                'action': 'error',
                'message': f"Sorry, I couldn't create that task. Error: {str(e)}"
            }
    
    def _handle_view_tasks(self, user_input: str) -> Dict:
        """
        Handle task viewing requests
        
        Args:
            user_input (str): User's task viewing request
            
        Returns:
            Dict: Response with task list
        """
        try:
            # Get task summary
            summary = self.task_manager.get_tasks_summary()
            
            # Generate AI response based on task summary
            if summary['total'] == 0:
                ai_response = "You don't have any tasks yet. Would you like to create one?"
            elif summary['pending'] == 0:
                ai_response = "Great! You've completed all your tasks. You're all caught up!"
            else:
                ai_response = f"You have {summary['pending']} pending tasks. "
                if summary['overdue'] > 0:
                    ai_response += f"⚠️ {summary['overdue']} are overdue. "
                if summary['due_today'] > 0:
                    ai_response += f"📅 {summary['due_today']} are due today."
            
            return {
                'action': 'tasks_displayed',
                'message': ai_response,
                'summary': summary if summary else {}
            }
            
        except Exception as e:
            return {
                'action': 'error',
                'message': f"Sorry, I couldn't retrieve your tasks. Error: {str(e)}"
            }
    
    def _handle_complete_task(self, user_input: str) -> Dict:
        """
        Handle task completion requests
        
        Args:
            user_input (str): User's task completion request
            
        Returns:
            Dict: Response with completion result
        """
        try:
            # Extract task ID or name from input
            task_id = self._extract_task_reference(user_input)
            
            if task_id:
                # Mark task as complete
                success = self.task_manager.mark_task_complete(task_id)
                
                if success:
                    ai_response = f"Great! Task {task_id} has been marked as completed. Well done! 🎉"
                    return {
                        'action': 'task_completed',
                        'message': ai_response,
                        'task_id': task_id
                    }
                else:
                    return {
                        'action': 'error',
                        'message': f"Sorry, I couldn't find task {task_id} to mark as complete."
                    }
            else:
                return {
                    'action': 'error',
                    'message': "I couldn't identify which task you want to complete. Please specify the task ID or name."
                }
                
        except Exception as e:
            return {
                'action': 'error',
                'message': f"Sorry, I couldn't complete that task. Error: {str(e)}"
            }
    
    def _handle_delete_task(self, user_input: str) -> Dict:
        """
        Handle task deletion requests
        
        Args:
            user_input (str): User's task deletion request
            
        Returns:
            Dict: Response with deletion result
        """
        try:
            # Extract task ID or name from input
            task_id = self._extract_task_reference(user_input)
            
            if task_id:
                # Delete task
                success = self.task_manager.delete_task(task_id)
                
                if success:
                    ai_response = f"Task {task_id} has been deleted successfully."
                    return {
                        'action': 'task_deleted',
                        'message': ai_response,
                        'task_id': task_id
                    }
                else:
                    return {
                        'action': 'error',
                        'message': f"Sorry, I couldn't find task {task_id} to delete."
                    }
            else:
                return {
                    'action': 'error',
                    'message': "I couldn't identify which task you want to delete. Please specify the task ID or name."
                }
                
        except Exception as e:
            return {
                'action': 'error',
                'message': f"Sorry, I couldn't delete that task. Error: {str(e)}"
            }
    
    def _handle_general_chat(self, user_input: str) -> Dict:
        """
        Handle general conversation and questions
        
        Args:
            user_input (str): User's general input
            
        Returns:
            Dict: Response with AI-generated message
        """
        try:
            # Generate AI response using LangChain
            ai_response = self._generate_ai_response(user_input)
            
            return {
                'action': 'general_response',
                'message': ai_response
            }
            
        except Exception as e:
            return {
                'action': 'error',
                'message': f"Sorry, I encountered an error: {str(e)}"
            }
    
    def _handle_unknown_request(self, user_input: str) -> Dict:
        """
        Handle requests that don't fit into known categories
        
        Args:
            user_input (str): User's input
            
        Returns:
            Dict: Response asking for clarification
        """
        return {
            'action': 'clarification_needed',
            'message': "I'm not sure what you'd like me to do. You can ask me to:\n"
                      "- Create a task (e.g., 'Remind me to call mom at 3 PM')\n"
                      "- Show your tasks (e.g., 'What's on my to-do list?')\n"
                      "- Complete a task (e.g., 'Mark task 1 as done')\n"
                      "- Delete a task (e.g., 'Delete task 2')\n"
                      "- Or just chat with me!"
        }
    
    def _extract_task_reference(self, user_input: str) -> Optional[int]:
        """
        Extract task ID or name from user input
        
        Args:
            user_input (str): User input containing task reference
            
        Returns:
            Optional[int]: Task ID if found, None otherwise
        """
        import re
        
        # Look for task ID patterns (e.g., "task 1", "task #1", "#1")
        id_patterns = [
            r'task\s*#?(\d+)',
            r'#(\d+)',
            r'(\d+)'
        ]
        
        for pattern in id_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _generate_ai_response(self, user_input: str, context: str = "") -> str:
        """
        Generate AI response using OpenAI and LangChain
        
        Args:
            user_input (str): User's input
            context (str): Additional context for the AI
            
        Returns:
            str: AI-generated response
        """
        try:
            # Prepare messages for the AI
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"User: {user_input}\nContext: {context}")
            ]
            
            # Get AI response
            response = self.llm(messages)
            
            # Store in memory for context
            self.memory.save_context(
                {"input": user_input},
                {"output": response.content}
            )
            
            return response.content
            
        except Exception as e:
            return f"I'm having trouble processing your request right now. Please try again later. Error: {str(e)}"
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get the conversation history from memory
        
        Returns:
            List[Dict]: List of conversation messages
        """
        try:
            # Get chat history from memory
            history = self.memory.chat_memory.messages
            
            # Convert to list of dictionaries
            conversation = []
            for message in history:
                conversation.append({
                    'type': message.__class__.__name__,
                    'content': message.content
                })
            
            return conversation
            
        except Exception as e:
            return []
    
    def clear_conversation_history(self):
        """
        Clear the conversation history
        """
        self.memory.clear()
