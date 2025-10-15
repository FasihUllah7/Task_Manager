"""
Database module for Personal Assistant
Handles SQLite database operations for task storage and retrieval
"""

import sqlite3  # SQLite database connector
import os       # Operating system interface for file operations
from datetime import datetime  # Date and time handling
from typing import List, Dict, Optional  # Type hints for better code documentation


class TaskDatabase:
    """
    SQLite database manager for storing and managing tasks
    Provides CRUD operations for task management
    """
    
    def __init__(self, db_path: str = "tasks.db"):
        """
        Initialize the database connection and create tables if they don't exist
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path  # Store database file path
        self.init_database()    # Initialize database tables
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Create and return a database connection
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        # Create connection to SQLite database
        conn = sqlite3.connect(self.db_path)
        # Enable row factory to return dictionaries instead of tuples
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """
        Initialize database by creating the tasks table if it doesn't exist
        """
        with self.get_connection() as conn:
            # Create tasks table with all necessary columns
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique task identifier
                    title TEXT NOT NULL,                   -- Task title/description
                    description TEXT,                      -- Additional task details
                    due_date TEXT,                         -- Due date in ISO format
                    priority TEXT DEFAULT 'medium',        -- Task priority (low, medium, high)
                    status TEXT DEFAULT 'pending',         -- Task status (pending, completed, cancelled)
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,  -- Creation timestamp
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP   -- Last update timestamp
                )
            """)
            conn.commit()  # Save changes to database
    
    def add_task(self, title: str, description: str = "", due_date: str = None, 
                 priority: str = "medium") -> int:
        """
        Add a new task to the database
        
        Args:
            title (str): Task title
            description (str): Task description
            due_date (str): Due date in ISO format (YYYY-MM-DD HH:MM:SS)
            priority (str): Task priority (low, medium, high)
            
        Returns:
            int: ID of the newly created task
        """
        with self.get_connection() as conn:
            # Insert new task into database
            cursor = conn.execute("""
                INSERT INTO tasks (title, description, due_date, priority)
                VALUES (?, ?, ?, ?)
            """, (title, description, due_date, priority))
            conn.commit()  # Save changes
            return cursor.lastrowid  # Return the ID of the new task
    
    def get_tasks(self, status: str = None, priority: str = None) -> List[Dict]:
        """
        Retrieve tasks from database with optional filtering
        
        Args:
            status (str): Filter by task status (pending, completed, cancelled)
            priority (str): Filter by task priority (low, medium, high)
            
        Returns:
            List[Dict]: List of task dictionaries
        """
        with self.get_connection() as conn:
            # Base query to get all tasks
            query = "SELECT * FROM tasks"
            params = []
            
            # Add WHERE clause if filters are provided
            if status or priority:
                conditions = []
                if status:
                    conditions.append("status = ?")
                    params.append(status)
                if priority:
                    conditions.append("priority = ?")
                    params.append(priority)
                query += " WHERE " + " AND ".join(conditions)
            
            # Order by creation date (newest first)
            query += " ORDER BY created_at DESC"
            
            # Execute query and return results as list of dictionaries
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """
        Retrieve a specific task by its ID
        
        Args:
            task_id (int): Task ID to retrieve
            
        Returns:
            Optional[Dict]: Task dictionary if found, None otherwise
        """
        with self.get_connection() as conn:
            # Get task by ID
            cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_task(self, task_id: int, title: str = None, description: str = None,
                   due_date: str = None, priority: str = None, status: str = None) -> bool:
        """
        Update an existing task
        
        Args:
            task_id (int): ID of task to update
            title (str): New task title
            description (str): New task description
            due_date (str): New due date
            priority (str): New priority level
            status (str): New status
            
        Returns:
            bool: True if task was updated, False if task not found
        """
        with self.get_connection() as conn:
            # Build dynamic UPDATE query based on provided parameters
            updates = []
            params = []
            
            if title is not None:
                updates.append("title = ?")
                params.append(title)
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            if due_date is not None:
                updates.append("due_date = ?")
                params.append(due_date)
            if priority is not None:
                updates.append("priority = ?")
                params.append(priority)
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            
            # Add updated timestamp
            updates.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            
            # Add task ID for WHERE clause
            params.append(task_id)
            
            # Execute update query
            cursor = conn.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()
            return cursor.rowcount > 0  # Return True if any rows were updated
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the database
        
        Args:
            task_id (int): ID of task to delete
            
        Returns:
            bool: True if task was deleted, False if task not found
        """
        with self.get_connection() as conn:
            # Delete task by ID
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0  # Return True if any rows were deleted
    
    def get_tasks_due_today(self) -> List[Dict]:
        """
        Get all tasks that are due today
        
        Returns:
            List[Dict]: List of tasks due today
        """
        today = datetime.now().strftime("%Y-%m-%d")  # Get today's date in YYYY-MM-DD format
        with self.get_connection() as conn:
            # Get tasks due today (matching date part only)
            cursor = conn.execute("""
                SELECT * FROM tasks 
                WHERE date(due_date) = ? AND status = 'pending'
                ORDER BY due_date ASC
            """, (today,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_overdue_tasks(self) -> List[Dict]:
        """
        Get all tasks that are overdue (due date has passed)
        
        Returns:
            List[Dict]: List of overdue tasks
        """
        now = datetime.now().isoformat()  # Current timestamp
        with self.get_connection() as conn:
            # Get tasks where due_date is in the past and status is pending
            cursor = conn.execute("""
                SELECT * FROM tasks 
                WHERE due_date < ? AND status = 'pending'
                ORDER BY due_date ASC
            """, (now,))
            return [dict(row) for row in cursor.fetchall()]
