#!/usr/bin/env python3
"""
Knowledge Base for Sahayak - Instant knowledge support for student questions
"""

import google.generativeai as genai
import os
import json
from typing import Dict, Any, List
from datetime import datetime

class KnowledgeBase:
    """Provide instant knowledge support for student questions"""
    
    def __init__(self, api_key: str = None):
        """Initialize the knowledge base"""
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
        
        self.common_questions = {
            'science': [
                'why is the sky blue',
                'how do plants grow',
                'what is photosynthesis',
                'why do we need water',
                'how do animals breathe'
            ],
            'mathematics': [
                'why do we need math',
                'how do we add numbers',
                'what are fractions',
                'why is zero important',
                'how do we measure things'
            ],
            'general': [
                'how do we learn',
                'why do we go to school',
                'what is the importance of education',
                'how do we make friends',
                'why do we need to study'
            ]
        }
    
    def get_answer(self, user_message: str) -> str:
        """Get answer to student question in appropriate language"""
        try:
            # Parse the question
            language, question, grade_level = self._parse_question(user_message)
            
            # Generate appropriate answer
            answer = self._generate_answer(question, language, grade_level)
            
            return answer
            
        except Exception as e:
            return f"Sorry, I couldn't find an answer. Error: {str(e)}"
    
    def _parse_question(self, user_message: str) -> tuple:
        """Parse user message to extract language, question, and grade level"""
        user_message_lower = user_message.lower()
        
        # Detect language
        language = 'english'  # default
        for lang_code, lang_name in self.supported_languages.items():
            if lang_code in user_message_lower or lang_name.lower() in user_message_lower:
                language = lang_code
                break
        
        # Detect grade level
        grade_level = 'grade_5'  # default
        for i in range(1, 11):
            if f'grade_{i}' in user_message_lower:
                grade_level = f'grade_{i}'
                break
        
        # Extract the actual question
        question = user_message
        if 'question:' in user_message_lower:
            question = user_message.split('question:')[-1].strip()
        elif 'asked:' in user_message_lower:
            question = user_message.split('asked:')[-1].strip()
        
        return language, question, grade_level
    
    def _generate_answer(self, question: str, language: str, grade_level: str) -> str:
        """Generate age-appropriate answer in the specified language"""
        grade_num = grade_level.split('_')[1]
        
        prompt = f"""
        Answer the following student question in {self.supported_languages[language]} 
        that is appropriate for Grade {grade_num} students:
        
        Question: {question}
        
        Requirements:
        1. Use simple, age-appropriate language for Grade {grade_num}
        2. Include real-world examples from Indian context
        3. Use analogies that students can understand
        4. Break down complex concepts into simple parts
        5. Include visual descriptions for blackboard use
        6. Make it engaging and interesting
        7. Include follow-up questions to encourage curiosity
        8. Use culturally relevant examples
        
        Format:
        - Start with a simple, direct answer
        - Include an analogy or example
        - Add a fun fact or interesting detail
        - End with a question to encourage further learning
        
        Answer should be written in {self.supported_languages[language]} with English translation if needed.
        Keep it under 150 words.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def get_common_questions(self, subject: str = None) -> Dict[str, List[str]]:
        """Get list of common questions by subject"""
        if subject:
            return {subject: self.common_questions.get(subject, [])}
        return self.common_questions
    
    def suggest_questions(self, topic: str) -> List[str]:
        """Suggest related questions for a given topic"""
        try:
            prompt = f"""
            Suggest 5 simple, age-appropriate questions that students might ask about "{topic}".
            Make them engaging and curiosity-driven.
            Format as a simple list.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.split('\n')
            
        except Exception as e:
            return [f"Error generating questions: {str(e)}"]
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages 