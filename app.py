"""
Main Streamlit application for Personal Assistant
Provides a web-based interface for task management using natural language
"""

import streamlit as st  # Streamlit web framework
import os  # Operating system interface
import random  # Random number generation for quote selection
from datetime import datetime  # Date and time handling
from dotenv import load_dotenv  # Load environment variables
from task_manager import TaskManager  # Import task manager
from ai_assistant import AIAssistant  # Import AI assistant
from database import TaskDatabase  # Import database for direct access


def get_motivational_quotes():
    """
    Get a list of motivational quotes for task management
    
    Returns:
        List[str]: List of motivational quotes
    """
    quotes = [
        "🌟 Every great achievement was once considered impossible.",
        "🚀 The way to get started is to quit talking and begin doing.",
        "💪 Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "🎯 The future belongs to those who believe in the beauty of their dreams.",
        "⭐ Don't watch the clock; do what it does. Keep going.",
        "🔥 The only way to do great work is to love what you do.",
        "🌈 Your limitation—it's only your imagination.",
        "⚡ Push yourself, because no one else is going to do it for you.",
        "🎪 Great things never come from comfort zones.",
        "🏆 Dream it. Wish it. Do it.",
        "💎 Success doesn't just find you. You have to go out and get it.",
        "🌟 The harder you work for something, the greater you'll feel when you achieve it.",
        "🚀 Dream bigger. Do bigger.",
        "💪 Don't stop when you're tired. Stop when you're done.",
        "🎯 Wake up with determination. Go to bed with satisfaction.",
        "⭐ Do something today that your future self will thank you for.",
        "🔥 Little things make big days.",
        "🌈 It's going to be hard, but hard does not mean impossible.",
        "⚡ Don't wait for opportunity. Create it.",
        "🎪 Sometimes we're tested not to show our weaknesses, but to discover our strengths.",
        "🏆 The key to success is to focus on goals, not obstacles.",
        "💎 Dream it. Believe it. Build it.",
        "🌟 What lies behind us and what lies before us are tiny matters compared to what lies within us.",
        "🚀 The only impossible journey is the one you never begin.",
        "💪 In the middle of difficulty lies opportunity.",
        "🎯 It does not matter how slowly you go as long as you do not stop.",
        "⭐ Life is 10% what happens to you and 90% how you react to it.",
        "🔥 The way to get started is to quit talking and begin doing.",
        "🌈 Life is what happens to you while you're busy making other plans.",
        "⚡ The future depends on what you do today.",
        "🎪 It is during our darkest moments that we must focus to see the light.",
        "🏆 The only way to do great work is to love what you do.",
        "💎 If you are working on something that you really care about, you don't have to be pushed. The vision pulls you.",
        "🌟 People who are crazy enough to think they can change the world, are the ones who do.",
        "🚀 We may encounter many defeats but we must not be defeated.",
        "💪 The person who says it cannot be done should not interrupt the person who is doing it.",
        "🎯 There are no traffic jams along the extra mile.",
        "⭐ It is never too late to be what you might have been.",
        "🔥 I am not a product of my circumstances. I am a product of my decisions.",
        "🌈 Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.",
        "⚡ A person who never made a mistake never tried anything new.",
        "🎪 I have not failed. I've just found 10,000 ways that won't work.",
        "🏆 If you want to lift yourself up, lift up someone else.",
        "💎 I would rather die of passion than of boredom.",
        "🌟 Life is either a daring adventure or nothing at all.",
        "🚀 What we achieve inwardly will change outer reality.",
        "💪 The only impossible journey is the one you never begin.",
        "🎯 In the middle of difficulty lies opportunity.",
        "⭐ It does not matter how slowly you go as long as you do not stop.",
        "🔥 Life is 10% what happens to you and 90% how you react to it."
    ]
    return quotes


def get_daily_quote():
    """
    Get a random motivational quote for the day
    Can be time-aware or context-aware based on user's task status
    
    Returns:
        str: A motivational quote
    """
    quotes = get_motivational_quotes()
    
    # Get current hour for time-aware quotes
    current_hour = datetime.now().hour
    
    # Get task summary for context-aware quotes
    try:
        summary = st.session_state.task_manager.get_tasks_summary()
        
        # Context-aware quotes based on task status
        if summary['overdue'] > 0:
            overdue_quotes = [
                "⏰ It's never too late to start fresh. Let's tackle those overdue tasks!",
                "🔄 Every moment is a new beginning. Time to catch up!",
                "💪 Challenges are what make life interesting. Overcoming them is what makes life meaningful.",
                "🌟 The best time to plant a tree was 20 years ago. The second best time is now."
            ]
            return random.choice(overdue_quotes)
        
        elif summary['pending'] == 0:
            completion_quotes = [
                "🎉 Congratulations! You've completed all your tasks. You're amazing!",
                "🏆 Well done! All tasks completed. Time to celebrate!",
                "⭐ You did it! Every task is done. You're a productivity superstar!",
                "🌟 Outstanding work! You've conquered your to-do list!"
            ]
            return random.choice(completion_quotes)
        
        elif summary['due_today'] > 0:
            today_quotes = [
                "📅 Today is the day! Let's make it count.",
                "⚡ Today's accomplishments were yesterday's impossibilities.",
                "🎯 Focus on today, and tomorrow will take care of itself.",
                "🔥 Make today so awesome that yesterday gets jealous!"
            ]
            return random.choice(today_quotes)
        
        # Time-aware quotes
        elif current_hour < 6:
            morning_quotes = [
                "🌅 Early bird catches the worm! Great start to your day!",
                "☀️ The sun is rising, and so are your possibilities!",
                "🌄 Every sunrise is a new opportunity to shine!",
                "🌟 Morning is when the magic happens!"
            ]
            return random.choice(morning_quotes)
        
        elif current_hour < 12:
            morning_quotes = [
                "☀️ Good morning! Let's make today productive!",
                "🌅 Rise and shine! Your tasks are waiting!",
                "☕ Morning coffee and morning tasks - perfect combination!",
                "🌟 Today is a blank page. Write a great story!"
            ]
            return random.choice(morning_quotes)
        
        elif current_hour < 18:
            afternoon_quotes = [
                "🌞 Afternoon energy! Keep the momentum going!",
                "⚡ Power through the afternoon like a champion!",
                "🎯 Afternoon focus time - let's get things done!",
                "💪 The afternoon is your time to shine!"
            ]
            return random.choice(afternoon_quotes)
        
        else:
            evening_quotes = [
                "🌙 Evening reflection time. How did today go?",
                "⭐ End the day with accomplishment, not regret.",
                "🌆 Evening is perfect for wrapping up loose ends.",
                "🌟 Finish strong! Tomorrow's success starts today."
            ]
            return random.choice(evening_quotes)
    
    except:
        # Fallback to random quote if there's any error
        pass
    
    # Default random quote
    return random.choice(quotes)


def initialize_app():
    """
    Initialize the application components and session state
    """
    # Load environment variables
    load_dotenv()
    
    # Initialize session state variables if they don't exist
    if 'task_manager' not in st.session_state:
        st.session_state.task_manager = TaskManager()
    
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant(st.session_state.task_manager)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'chat'
    
    # Initialize daily quote if not set or if it's a new day
    current_date = datetime.now().strftime("%Y-%m-%d")
    if 'daily_quote' not in st.session_state or 'quote_date' not in st.session_state or st.session_state.quote_date != current_date:
        st.session_state.daily_quote = get_daily_quote()
        st.session_state.quote_date = current_date


def display_header():
    """
    Display the application header and title
    """
    # Set page configuration
    st.set_page_config(
        page_title="Task Manager",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Display main title
    st.title("Daily Task Manager")
    st.markdown("**Manage your daily tasks with ease**")
    
    # Display motivational quote in a highlighted box
    st.markdown("---")
    
    # Create columns for quote and refresh button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            ">
                <h3 style="color: white; margin: 0; font-size: 1.2em; font-weight: 300;">
                    {st.session_state.daily_quote}
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        if st.button("🔄", help="Get a new motivational quote", key="refresh_quote"):
            st.session_state.daily_quote = get_daily_quote()
            st.rerun()
    
    st.markdown("---")
    
    # Display description
    st.markdown("""
    Welcome to your personal Task Manager:
    
    """)


def display_sidebar():
    """
    Display the sidebar with navigation and task summary
    """
    with st.sidebar:
        st.header("📊 Dashboard")
        
        # Get task summary
        try:
            summary = st.session_state.task_manager.get_tasks_summary()
            
            # Display task statistics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Tasks", summary['total'])
                st.metric("Pending", summary['pending'])
            with col2:
                st.metric("Completed", summary['completed'])
                st.metric("Overdue", summary['overdue'])
            
            # Display overdue tasks warning
            if summary['overdue'] > 0:
                st.warning(f"⚠️ You have {summary['overdue']} overdue tasks!")
            
            # Display tasks due today
            if summary['due_today'] > 0:
                st.info(f"📅 {summary['due_today']} tasks due today")
            
        except Exception as e:
            st.error(f"Error loading task summary: {str(e)}")
        
        st.markdown("---")
        
        # Navigation buttons
        st.header("🧭 Navigation")
        if st.button("💬 Chat with Assistant", use_container_width=True):
            st.session_state.current_view = 'chat'
        
        if st.button("📋 View All Tasks", use_container_width=True):
            st.session_state.current_view = 'tasks'
        
        if st.button("➕ Quick Add Task", use_container_width=True):
            st.session_state.current_view = 'add_task'
        
        # Clear chat history button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.ai_assistant.clear_conversation_history()
            st.rerun()


def display_chat_interface():
    """
    Display the main chat interface
    """
    st.header("💬 Chat with Your Assistant")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        # Show previous messages
        for message in st.session_state.chat_history:
            if message['type'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])
                    
                    # Display task information if available and not None
                    if 'task' in message and message['task'] is not None:
                        display_task_card(message['task'])
                    elif 'summary' in message and message['summary'] is not None:
                        display_task_summary(message['summary'])
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({
            'type': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Process user input with AI assistant
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.ai_assistant.process_user_input(user_input)
                
                # Add assistant response to chat history
                st.session_state.chat_history.append({
                    'type': 'assistant',
                    'content': response.get('message', 'No response'),
                    'action': response.get('action', 'unknown'),
                    'task': response.get('task'),
                    'summary': response.get('summary'),
                    'timestamp': datetime.now()
                })
                
                # Check if task was completed and refresh quote
                if response.get('action') == 'task_completed':
                    st.session_state.daily_quote = get_daily_quote()
                
            except Exception as e:
                st.session_state.chat_history.append({
                    'type': 'assistant',
                    'content': f"Sorry, I encountered an error: {str(e)}",
                    'timestamp': datetime.now()
                })
        
        # Rerun to update the interface
        st.rerun()


def display_task_card(task):
    """
    Display a task card with task information
    
    Args:
        task (dict): Task dictionary with task details
    """
    # Check if task is valid
    if not task or not isinstance(task, dict):
        st.error("Invalid task data")
        return
    
    with st.expander(f"📝 Task #{task['id']}: {task['title']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Description:** {task['description'] or 'No description'}")
            st.write(f"**Priority:** {task['priority'].title()}")
            st.write(f"**Status:** {task['status'].title()}")
        
        with col2:
            if task['due_date']:
                due_date = datetime.fromisoformat(task['due_date'])
                st.write(f"**Due Date:** {due_date.strftime('%Y-%m-%d %H:%M')}")
            else:
                st.write("**Due Date:** No due date")
            
            st.write(f"**Created:** {task['created_at']}")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"✅ Complete", key=f"complete_{task['id']}"):
                st.session_state.task_manager.mark_task_complete(task['id'])
                # Refresh quote to show completion message
                st.session_state.daily_quote = get_daily_quote()
                st.success("Task marked as complete!")
                st.rerun()
        
        with col2:
            if st.button(f"🗑️ Delete", key=f"delete_{task['id']}"):
                st.session_state.task_manager.delete_task(task['id'])
                st.success("Task deleted!")
                st.rerun()
        
        with col3:
            if st.button(f"📝 Edit", key=f"edit_{task['id']}"):
                st.session_state.editing_task = task['id']
                st.rerun()


def display_task_summary(summary):
    """
    Display task summary information
    
    Args:
        summary (dict): Task summary dictionary
    """
    # Check if summary is valid
    if not summary or not isinstance(summary, dict):
        st.error("Invalid summary data")
        return
    
    if summary['pending_tasks']:
        st.subheader("📋 Pending Tasks")
        for task in summary['pending_tasks']:
            display_task_card(task)
    
    if summary['overdue_tasks']:
        st.subheader("⚠️ Overdue Tasks")
        for task in summary['overdue_tasks']:
            display_task_card(task)
    
    if summary['today_tasks']:
        st.subheader("📅 Tasks Due Today")
        for task in summary['today_tasks']:
            display_task_card(task)


def display_tasks_view():
    """
    Display the tasks management view
    """
    st.header("📋 Task Management")
    
    # Get all tasks
    try:
        all_tasks = st.session_state.task_manager.db.get_tasks()
        
        if not all_tasks:
            st.info("No tasks found. Create your first task using the chat interface!")
            return
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Pending", "Completed", "Cancelled"]
            )
        with col2:
            priority_filter = st.selectbox(
                "Filter by Priority",
                ["All", "High", "Medium", "Low"]
            )
        with col3:
            sort_by = st.selectbox(
                "Sort by",
                ["Created Date", "Due Date", "Priority", "Title"]
            )
        
        # Apply filters
        filtered_tasks = all_tasks
        if status_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t['status'].lower() == status_filter.lower()]
        if priority_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t['priority'].lower() == priority_filter.lower()]
        
        # Sort tasks
        if sort_by == "Created Date":
            filtered_tasks.sort(key=lambda x: x['created_at'], reverse=True)
        elif sort_by == "Due Date":
            filtered_tasks.sort(key=lambda x: x['due_date'] or '9999-12-31')
        elif sort_by == "Priority":
            priority_order = {'high': 3, 'medium': 2, 'low': 1}
            filtered_tasks.sort(key=lambda x: priority_order.get(x['priority'], 0), reverse=True)
        elif sort_by == "Title":
            filtered_tasks.sort(key=lambda x: x['title'].lower())
        
        # Display filtered tasks
        st.write(f"Showing {len(filtered_tasks)} tasks")
        
        for task in filtered_tasks:
            display_task_card(task)
            
    except Exception as e:
        st.error(f"Error loading tasks: {str(e)}")


def display_add_task_view():
    """
    Display the quick add task view
    """
    st.header("➕ Quick Add Task")
    
    # Task input form
    with st.form("add_task_form"):
        task_title = st.text_input("Task Title", placeholder="e.g., Call mom at 3 PM")
        task_description = st.text_area("Description (optional)", placeholder="Additional details...")
        
        col1, col2 = st.columns(2)
        with col1:
            due_date = st.date_input("Due Date (optional)")
            due_time = st.time_input("Due Time (optional)")
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        
        submitted = st.form_submit_button("Add Task", use_container_width=True)
        
        if submitted and task_title:
            try:
                # Combine date and time if both are provided
                due_datetime = None
                if due_date and due_time:
                    due_datetime = datetime.combine(due_date, due_time).isoformat()
                elif due_date:
                    due_datetime = datetime.combine(due_date, datetime.min.time()).isoformat()
                
                # Add task to database
                task_id = st.session_state.task_manager.db.add_task(
                    title=task_title,
                    description=task_description,
                    due_date=due_datetime,
                    priority=priority.lower()
                )
                
                st.success(f"Task added successfully! Task ID: {task_id}")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error adding task: {str(e)}")


def main():
    """
    Main application function
    """
    # Initialize the application
    initialize_app()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Check if all tasks are completed and show celebration
    try:
        summary = st.session_state.task_manager.get_tasks_summary()
        if summary['pending'] == 0 and summary['total'] > 0:
            st.balloons()
            st.success("🎉 Congratulations! You've completed all your tasks! You're amazing! 🎉")
    except:
        pass
    
    # Main content area based on current view
    if st.session_state.current_view == 'chat':
        display_chat_interface()
    elif st.session_state.current_view == 'tasks':
        display_tasks_view()
    elif st.session_state.current_view == 'add_task':
        display_add_task_view()
    
    # Footer
    st.markdown("---")


if __name__ == "__main__":
    main()
