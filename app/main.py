from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime
import re

from .assistant import SahayakAssistant
from .data_loader import DataLoader
# from .utils import save_conversation_log  # Removed, function does not exist
from .config import config

# Initialize Flask app
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Get configuration
env = os.getenv('FLASK_ENV', 'development')
app_config = config.get(env, config['default'])
app.config.from_object(app_config)

# Configure logging
# Ensure responses directory exists
os.makedirs('../responses', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../responses/logs.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize components
data_loader = DataLoader()
sahayak_assistant = SahayakAssistant()

@app.route('/')
def index():
    """Home page with the chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and return AI responses"""
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Please enter a message'
            }), 400
        
        # Input validation and sanitization
        if len(user_message) > 1000:
            return jsonify({
                'success': False,
                'error': 'Message too long. Please keep it under 1000 characters.'
            }), 400
        
        # Basic XSS protection
        if re.search(r'<script|javascript:|on\w+\s*=', user_message, re.IGNORECASE):
            return jsonify({
                'success': False,
                'error': 'Invalid input detected.'
            }), 400
        
        # Load user data
        user_data = data_loader.load_data()
        
        # Get AI response (this may update the data)
        ai_response = sahayak_assistant.get_response(user_message, user_data)
        
        # Reload data in case it was updated
        user_data = data_loader.load_data()
        
        # Save conversation log
        # save_conversation_log(user_message, ai_response)  # Removed, function does not exist
        
        # Log the interaction
        logger.info(f"User: {user_message[:100]}...")
        logger.info(f"AI: {ai_response[:100]}...")
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error. Please try again.'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error. Please try again later.'
    }), 500

if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        logger.error("GEMINI_API_KEY not found in environment variables")
        exit(1)
    
    logger.info("Starting Sahayak AI Teaching Assistant Flask Application")
    app.run(debug=True, host='0.0.0.0', port=5000)
