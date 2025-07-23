#!/usr/bin/env python3
"""
Content Generator for Sahayak - Hyper-local content generation in Indian languages
"""

import google.generativeai as genai
import os
import json
from typing import Dict, Any, List
from datetime import datetime

class ContentGenerator:
    """Generate hyper-local content in Indian languages"""
    
    def __init__(self, api_key: str = None):
        """Initialize the content generator"""
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.supported_languages = {
            'hindi': 'हिंदी',
            'marathi': 'मराठी', 
            'tamil': 'தமிழ்',
            'telugu': 'తెలుగు',
            'bengali': 'বাংলা',
            'gujarati': 'ગુજરાતી',
            'kannada': 'ಕನ್ನಡ',
            'malayalam': 'മലയാളം',
            'punjabi': 'ਪੰਜਾਬੀ',
            'english': 'English'
        }
        
        self.grade_levels = {
            'grade_1': 'Primary (6-7 years)',
            'grade_2': 'Primary (7-8 years)',
            'grade_3': 'Primary (8-9 years)',
            'grade_4': 'Primary (9-10 years)',
            'grade_5': 'Primary (10-11 years)',
            'grade_6': 'Upper Primary (11-12 years)',
            'grade_7': 'Upper Primary (12-13 years)',
            'grade_8': 'Upper Primary (13-14 years)',
            'grade_9': 'Secondary (14-15 years)',
            'grade_10': 'Secondary (15-16 years)'
        }
    
    def generate_content(self, user_message: str) -> str:
        """Generate localized content based on user request"""
        try:
            # Extract language and topic from message
            language, topic, context, grade_level = self._parse_content_request(user_message)
            
            # Generate appropriate content type
            if 'story' in user_message.lower():
                return self._generate_story(language, topic, context, grade_level)
            elif 'explanation' in user_message.lower() or 'explain' in user_message.lower():
                return self._generate_explanation(language, topic, context, grade_level)
            elif 'example' in user_message.lower():
                return self._generate_example(language, topic, context, grade_level)
            else:
                return self._generate_general_content(language, topic, context, grade_level)
                
        except Exception as e:
            return f"Sorry, I couldn't generate the content. Error: {str(e)}"
    
    def _parse_content_request(self, user_message: str) -> tuple:
        """Parse user message to extract language, topic, context, and grade level"""
        user_message_lower = user_message.lower()
        
        # Detect language
        language = 'english'  # default
        for lang_code, lang_name in self.supported_languages.items():
            if lang_code in user_message_lower or lang_name.lower() in user_message_lower:
                language = lang_code
                break
        
        # Detect grade level
        grade_level = 'grade_5'  # default
        for grade in self.grade_levels.keys():
            if grade in user_message_lower:
                grade_level = grade
                break
        
        # Extract topic and context (simplified parsing)
        topic = "general education"
        context = "classroom"
        
        # Look for common topics
        topics = ['soil types', 'water cycle', 'photosynthesis', 'addition', 'subtraction', 
                 'grammar', 'history', 'geography', 'science', 'mathematics', 'english']
        for t in topics:
            if t in user_message_lower:
                topic = t
                break
        
        # Look for context
        contexts = ['farmers', 'village', 'city', 'family', 'school', 'market', 'home']
        for c in contexts:
            if c in user_message_lower:
                context = c
                break
        
        return language, topic, context, grade_level
    
    def _generate_story(self, language: str, topic: str, context: str, grade_level: str) -> str:
        """Generate a culturally relevant story"""
        prompt = f"""
        Create a short, engaging story in {self.supported_languages[language]} about {topic} 
        that connects with {context} context. The story should be appropriate for {self.grade_levels[grade_level]}.
        
        Requirements:
        1. Use simple, age-appropriate language
        2. Include cultural elements relevant to Indian students
        3. Make it educational and engaging
        4. Include characters that students can relate to
        5. Keep it under 200 words
        6. Include a moral or learning point
        
        Story should be written in {self.supported_languages[language]} with English translation if needed.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _generate_explanation(self, language: str, topic: str, context: str, grade_level: str) -> str:
        """Generate a simple explanation"""
        prompt = f"""
        Create a simple explanation of {topic} in {self.supported_languages[language]} 
        that is appropriate for {self.grade_levels[grade_level]} students.
        
        Requirements:
        1. Use simple, clear language
        2. Include real-world examples from Indian context
        3. Use analogies that students can understand
        4. Break down complex concepts into simple parts
        5. Include visual descriptions for blackboard use
        6. Make it culturally relevant
        
        Explanation should be written in {self.supported_languages[language]} with English translation if needed.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _generate_example(self, language: str, topic: str, context: str, grade_level: str) -> str:
        """Generate practical examples"""
        prompt = f"""
        Create practical examples of {topic} in {self.supported_languages[language]} 
        that are relevant to {self.grade_levels[grade_level]} students and {context} context.
        
        Requirements:
        1. Use everyday situations students can relate to
        2. Include Indian cultural context
        3. Make examples age-appropriate
        4. Include step-by-step explanations
        5. Use simple language
        6. Provide multiple examples for different difficulty levels
        
        Examples should be written in {self.supported_languages[language]} with English translation if needed.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _generate_general_content(self, language: str, topic: str, context: str, grade_level: str) -> str:
        """Generate general educational content"""
        prompt = f"""
        Create educational content about {topic} in {self.supported_languages[language]} 
        for {self.grade_levels[grade_level]} students in a {context} context.
        
        Requirements:
        1. Make it engaging and interactive
        2. Include cultural elements
        3. Use age-appropriate language
        4. Include practical applications
        5. Make it suitable for multi-grade classrooms
        6. Include assessment questions
        
        Content should be written in {self.supported_languages[language]} with English translation if needed.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages
    
    def get_grade_levels(self) -> Dict[str, str]:
        """Get list of supported grade levels"""
        return self.grade_levels 