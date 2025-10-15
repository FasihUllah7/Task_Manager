"""
Setup script for Personal Assistant
Helps users initialize the application and check dependencies
"""

import os  # Operating system interface
import sys  # System-specific parameters and functions
import subprocess  # Subprocess management
import sqlite3  # SQLite database connector
from pathlib import Path  # Object-oriented filesystem paths


def check_python_version():
    """
    Check if Python version is 3.8 or higher
    
    Returns:
        bool: True if Python version is compatible, False otherwise
    """
    print("🐍 Checking Python version...")
    
    # Get Python version
    version = sys.version_info
    
    # Check if version is 3.8 or higher
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Please install Python 3.8 or higher")
        return False


def check_dependencies():
    """
    Check if required dependencies are installed
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    print("📦 Checking dependencies...")
    
    # List of required packages
    required_packages = [
        'streamlit',
        'openai',
        'langchain',
        'langchain-openai',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    # Check each package
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    # Install missing packages if any
    if missing_packages:
        print(f"\n📥 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
            ])
            print("✅ All dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("   Please run: pip install -r requirements.txt")
            return False
    
    print("✅ All dependencies are available")
    return True


def setup_environment():
    """
    Set up environment variables and configuration
    
    Returns:
        bool: True if environment is set up successfully, False otherwise
    """
    print("⚙️ Setting up environment...")
    
    # Check if .env file exists
    env_file = Path('.env')
    env_template = Path('env_template.txt')
    
    if not env_file.exists():
        if env_template.exists():
            print("📝 Creating .env file from template...")
            try:
                # Copy template to .env
                with open(env_template, 'r') as template:
                    content = template.read()
                
                with open(env_file, 'w') as env:
                    env.write(content)
                
                print("✅ .env file created")
                print("⚠️  Please edit .env file and add your OpenAI API key")
                return False  # Return False to indicate user action needed
            except Exception as e:
                print(f"❌ Failed to create .env file: {e}")
                return False
        else:
            print("❌ env_template.txt not found")
            return False
    else:
        print("✅ .env file already exists")
    
    # Check if OpenAI API key is set
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your_openai_api_key_here':
            print("⚠️  OpenAI API key not set in .env file")
            print("   Please edit .env file and add your actual API key")
            return False
        else:
            print("✅ OpenAI API key is configured")
            return True
            
    except Exception as e:
        print(f"❌ Error checking environment: {e}")
        return False


def initialize_database():
    """
    Initialize the SQLite database
    
    Returns:
        bool: True if database is initialized successfully, False otherwise
    """
    print("🗄️ Initializing database...")
    
    try:
        # Import and initialize database
        from database import TaskDatabase
        
        # Create database instance (this will create the table if it doesn't exist)
        db = TaskDatabase()
        
        print("✅ Database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False


def run_application():
    """
    Run the Streamlit application
    
    Returns:
        bool: True if application starts successfully, False otherwise
    """
    print("🚀 Starting Personal Assistant...")
    
    try:
        # Start Streamlit application
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
        return True
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return True
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return False


def main():
    """
    Main setup function that runs all checks and setup steps
    """
    print("🤖 Personal Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    print()
    
    # Check and install dependencies
    if not check_dependencies():
        return
    
    print()
    
    # Set up environment
    env_ready = setup_environment()
    if not env_ready:
        print("\n⚠️  Setup incomplete. Please configure your .env file and run setup again.")
        return
    
    print()
    
    # Initialize database
    if not initialize_database():
        return
    
    print()
    print("✅ Setup completed successfully!")
    print("🚀 Starting Personal Assistant...")
    print("=" * 40)
    
    # Run the application
    run_application()


if __name__ == "__main__":
    main()
