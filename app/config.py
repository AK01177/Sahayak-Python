"""
Configuration settings for Sahayak application
AI Teaching Assistant for Indian Classrooms
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sahayak-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # AI Model settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    # Data settings
    DATA_FILE = 'data/personal_data.json'
    BACKUP_DIR = 'data/backups/'
    
    # Content settings
    MAX_RESPONSE_LENGTH = 2000
    SUPPORTED_LANGUAGES = [
        'english', 'hindi', 'gujarati', 'marathi', 
        'bengali', 'tamil', 'telugu', 'kannada', 'malayalam'
    ]
    
    # Subject settings
    SUPPORTED_SUBJECTS = [
        'mathematics', 'science', 'english', 'hindi', 
        'social_studies', 'computer_science'
    ]
    
    # Grade levels
    GRADE_LEVELS = [
        'Class 1-5', 'Class 6-8', 'Class 9-10', 'Class 11-12'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DATA_FILE = 'data/personal_data.json'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DATA_FILE = 'data/personal_data.json'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATA_FILE = 'data/test_data.json'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
