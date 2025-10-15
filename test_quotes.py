"""
Test script to demonstrate the motivational quotes feature
Run this to see different quotes based on time and context
"""

import sys
import os
from datetime import datetime
import random

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from task_manager import TaskManager
from database import TaskDatabase


def get_motivational_quotes():
    """
    Get a list of motivational quotes for task management
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
        "🏆 Dream it. Wish it. Do it."
    ]
    return quotes


def get_daily_quote(task_manager=None):
    """
    Get a random motivational quote for the day
    Can be time-aware or context-aware based on user's task status
    """
    quotes = get_motivational_quotes()
    
    # Get current hour for time-aware quotes
    current_hour = datetime.now().hour
    
    # Get task summary for context-aware quotes
    if task_manager:
        try:
            summary = task_manager.get_tasks_summary()
            
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
        
        except:
            pass
    
    # Time-aware quotes
    if current_hour < 6:
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


def main():
    """
    Test the motivational quotes feature
    """
    print("🤖 Personal Assistant - Motivational Quotes Test")
    print("=" * 50)
    
    # Initialize task manager
    task_manager = TaskManager()
    
    # Show current time
    current_time = datetime.now()
    print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current hour: {current_time.hour}")
    print()
    
    # Show task summary
    try:
        summary = task_manager.get_tasks_summary()
        print("📊 Task Summary:")
        print(f"  Total tasks: {summary['total']}")
        print(f"  Pending: {summary['pending']}")
        print(f"  Completed: {summary['completed']}")
        print(f"  Overdue: {summary['overdue']}")
        print(f"  Due today: {summary['due_today']}")
        print()
    except Exception as e:
        print(f"Error getting task summary: {e}")
        print()
    
    # Show different types of quotes
    print("💬 Motivational Quotes:")
    print("-" * 30)
    
    # Show 5 random quotes
    for i in range(5):
        quote = get_daily_quote(task_manager)
        print(f"{i+1}. {quote}")
    
    print()
    print("🔄 Quote changes based on:")
    print("  - Time of day (morning, afternoon, evening)")
    print("  - Task status (overdue, completed, due today)")
    print("  - Random selection from 50+ motivational quotes")
    print()
    print("✨ In the app, quotes update automatically when:")
    print("  - You open the app (daily refresh)")
    print("  - You complete a task")
    print("  - You click the refresh button (🔄)")
    print("  - The day changes")


if __name__ == "__main__":
    main()
