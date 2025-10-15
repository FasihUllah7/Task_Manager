"""
Task Manager module for Personal Assistant
Handles natural language processing and task management operations
"""

import re  # Regular expressions for text processing
from datetime import datetime, timedelta  # Date and time handling
from typing import Dict, List, Optional, Tuple  # Type hints
from database import TaskDatabase  # Import our database module


class TaskManager:
    """
    Main task management class that handles natural language processing
    and coordinates between the database and AI services
    """
    
    def __init__(self, db_path: str = "tasks.db"):
        """
        Initialize the task manager with database connection
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db = TaskDatabase(db_path)  # Initialize database connection
        self.priority_keywords = {  # Keywords to identify task priority
            'high': ['urgent', 'asap', 'immediately', 'critical', 'important', 'high'],
            'medium': ['normal', 'regular', 'medium'],
            'low': ['low', 'later', 'whenever', 'optional']
        }
    
    def parse_natural_language(self, user_input: str) -> Dict:
        """
        Parse natural language input to extract task information
        
        Args:
            user_input (str): User's natural language input
            
        Returns:
            Dict: Parsed task information including title, due_date, priority
        """
        # Convert input to lowercase for easier processing
        input_lower = user_input.lower()
        
        # Initialize result dictionary
        result = {
            'title': user_input.strip(),  # Default title is the full input
            'due_date': None,
            'priority': 'medium',  # Default priority
            'description': ''
        }
        
        # Extract due date information
        due_date = self._extract_due_date(input_lower)
        if due_date:
            result['due_date'] = due_date
            # Remove date information from title to clean it up
            result['title'] = self._clean_title_from_date(user_input, due_date)
        
        # Extract priority information
        priority = self._extract_priority(input_lower)
        if priority:
            result['priority'] = priority
        
        # Extract description if present (usually after "to" or "about")
        description = self._extract_description(user_input)
        if description:
            result['description'] = description
        
        return result
    
    def _extract_due_date(self, text: str) -> Optional[str]:
        """
        Extract due date from natural language text
        
        Args:
            text (str): Input text in lowercase
            
        Returns:
            Optional[str]: ISO formatted date string or None
        """
        now = datetime.now()  # Current timestamp
        
        # Pattern for "by [time]" (e.g., "by 5 PM", "by tomorrow")
        by_pattern = r'by\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?|tomorrow|today|next\s+\w+)'
        by_match = re.search(by_pattern, text)
        
        if by_match:
            time_str = by_match.group(1).strip()
            return self._parse_time_expression(time_str, now)
        
        # Pattern for "at [time]" (e.g., "at 3 PM", "at noon")
        at_pattern = r'at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?|noon|midnight)'
        at_match = re.search(at_pattern, text)
        
        if at_match:
            time_str = at_match.group(1).strip()
            return self._parse_time_expression(time_str, now)
        
        # Pattern for relative time (e.g., "in 2 hours", "in 30 minutes")
        relative_pattern = r'in\s+(\d+)\s+(minutes?|hours?|days?)'
        relative_match = re.search(relative_pattern, text)
        
        if relative_match:
            amount = int(relative_match.group(1))
            unit = relative_match.group(2)
            return self._calculate_relative_time(amount, unit, now)
        
        return None
    
    def _parse_time_expression(self, time_str: str, base_time: datetime) -> str:
        """
        Parse time expressions like "5 PM", "tomorrow", "noon"
        
        Args:
            time_str (str): Time expression to parse
            base_time (datetime): Base time for relative calculations
            
        Returns:
            str: ISO formatted datetime string
        """
        time_str = time_str.lower()
        
        # Handle "tomorrow"
        if time_str == 'tomorrow':
            tomorrow = base_time + timedelta(days=1)
            return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0).isoformat()
        
        # Handle "today"
        if time_str == 'today':
            return base_time.replace(hour=18, minute=0, second=0, microsecond=0).isoformat()
        
        # Handle "noon"
        if time_str == 'noon':
            return base_time.replace(hour=12, minute=0, second=0, microsecond=0).isoformat()
        
        # Handle "midnight"
        if time_str == 'midnight':
            return base_time.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        
        # Handle time patterns like "5 PM", "3:30 AM"
        time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?'
        time_match = re.match(time_pattern, time_str)
        
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2) or 0)
            period = time_match.group(3)
            
            # Convert to 24-hour format
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            # Set the time for today
            result_time = base_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, set for tomorrow
            if result_time <= base_time:
                result_time += timedelta(days=1)
            
            return result_time.isoformat()
        
        return None
    
    def _calculate_relative_time(self, amount: int, unit: str, base_time: datetime) -> str:
        """
        Calculate relative time from current time
        
        Args:
            amount (int): Number of units
            unit (str): Time unit (minutes, hours, days)
            base_time (datetime): Base time for calculation
            
        Returns:
            str: ISO formatted datetime string
        """
        if unit.startswith('minute'):
            delta = timedelta(minutes=amount)
        elif unit.startswith('hour'):
            delta = timedelta(hours=amount)
        elif unit.startswith('day'):
            delta = timedelta(days=amount)
        else:
            return None
        
        result_time = base_time + delta
        return result_time.isoformat()
    
    def _extract_priority(self, text: str) -> Optional[str]:
        """
        Extract priority level from text
        
        Args:
            text (str): Input text in lowercase
            
        Returns:
            Optional[str]: Priority level (high, medium, low) or None
        """
        for priority, keywords in self.priority_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return priority
        return None
    
    def _extract_description(self, text: str) -> str:
        """
        Extract task description from natural language
        
        Args:
            text (str): Input text
            
        Returns:
            str: Extracted description
        """
        # Look for patterns like "to [description]" or "about [description]"
        to_pattern = r'to\s+(.+?)(?:\s+by|\s+at|\s+in|$)'
        about_pattern = r'about\s+(.+?)(?:\s+by|\s+at|\s+in|$)'
        
        to_match = re.search(to_pattern, text, re.IGNORECASE)
        if to_match:
            return to_match.group(1).strip()
        
        about_match = re.search(about_pattern, text, re.IGNORECASE)
        if about_match:
            return about_match.group(1).strip()
        
        return ''
    
    def _clean_title_from_date(self, original_text: str, due_date: str) -> str:
        """
        Remove date/time information from title to make it cleaner
        
        Args:
            original_text (str): Original user input
            due_date (str): Extracted due date
            
        Returns:
            str: Cleaned title without date information
        """
        # Remove common date/time patterns
        patterns_to_remove = [
            r'\s+by\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?',
            r'\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?',
            r'\s+in\s+\d+\s+(?:minutes?|hours?|days?)',
            r'\s+by\s+tomorrow',
            r'\s+by\s+today',
            r'\s+at\s+noon',
            r'\s+at\s+midnight'
        ]
        
        cleaned_text = original_text
        for pattern in patterns_to_remove:
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
        
        return cleaned_text.strip()
    
    def add_task_from_natural_language(self, user_input: str) -> int:
        """
        Add a task from natural language input
        
        Args:
            user_input (str): User's natural language input
            
        Returns:
            int: ID of the created task
        """
        # Parse the natural language input
        parsed_task = self.parse_natural_language(user_input)
        
        # Add task to database
        task_id = self.db.add_task(
            title=parsed_task['title'],
            description=parsed_task['description'],
            due_date=parsed_task['due_date'],
            priority=parsed_task['priority']
        )
        
        return task_id
    
    def get_tasks_summary(self) -> Dict:
        """
        Get a summary of all tasks organized by status and priority
        
        Returns:
            Dict: Task summary with counts and lists
        """
        all_tasks = self.db.get_tasks()  # Get all tasks
        pending_tasks = self.db.get_tasks(status='pending')  # Get pending tasks
        completed_tasks = self.db.get_tasks(status='completed')  # Get completed tasks
        overdue_tasks = self.db.get_overdue_tasks()  # Get overdue tasks
        today_tasks = self.db.get_tasks_due_today()  # Get tasks due today
        
        return {
            'total': len(all_tasks),
            'pending': len(pending_tasks),
            'completed': len(completed_tasks),
            'overdue': len(overdue_tasks),
            'due_today': len(today_tasks),
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'today_tasks': today_tasks
        }
    
    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as completed
        
        Args:
            task_id (int): ID of task to mark as complete
            
        Returns:
            bool: True if task was updated, False if not found
        """
        return self.db.update_task(task_id, status='completed')
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task
        
        Args:
            task_id (int): ID of task to delete
            
        Returns:
            bool: True if task was deleted, False if not found
        """
        return self.db.delete_task(task_id)
    
    def update_task_priority(self, task_id: int, priority: str) -> bool:
        """
        Update task priority
        
        Args:
            task_id (int): ID of task to update
            priority (str): New priority level
            
        Returns:
            bool: True if task was updated, False if not found
        """
        return self.db.update_task(task_id, priority=priority)
