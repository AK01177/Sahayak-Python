#!/usr/bin/env python3
"""
Sahayak - AI Teaching Assistant
A multi-grade, multi-language educational assistant for Indian classrooms
"""

import os
import sys
from app.main import app

def main():
    """Main entry point for Sahayak application"""
    
    # Set up environment
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # Print startup message
    print("🚀 Starting Sahayak...")
    print("📚 AI Teaching Assistant for Indian Classrooms")
    print("🌐 Supporting multiple languages and subjects")
    print("=" * 50)
    
    try:
        # Run the Flask application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Sahayak stopped. Thanks for using the educational assistant!")
    except Exception as e:
        print(f"❌ Error starting Sahayak: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
