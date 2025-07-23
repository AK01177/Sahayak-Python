#!/usr/bin/env python3
"""
Worksheet Generator for Sahayak - Differentiated learning materials
"""

import google.generativeai as genai
import os
import json
from typing import Dict, Any, List
from datetime import datetime

class WorksheetGenerator:
    """Generate differentiated worksheets for multi-grade classrooms"""
    
    def __init__(self, api_key: str = None):
        """Initialize the worksheet generator"""
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.subjects = {
            'mathematics': ['addition', 'subtraction', 'multiplication', 'division', 'fractions', 'geometry'],
            'science': ['plants', 'animals', 'water cycle', 'solar system', 'human body', 'environment'],
            'english': ['grammar', 'vocabulary', 'reading', 'writing', 'comprehension', 'story writing'],
            'hindi': ['व्याकरण', 'शब्दावली', 'पठन', 'लेखन', 'कहानी लेखन'],
            'social_studies': ['history', 'geography', 'civics', 'economics', 'culture', 'current_affairs']
        }
        
        self.difficulty_levels = {
            'easy': 'Basic concepts, simple problems',
            'medium': 'Standard problems, moderate complexity',
            'hard': 'Advanced problems, critical thinking'
        }
    
    def generate_worksheets(self, user_message: str) -> str:
        """Generate differentiated worksheets based on user request"""
        try:
            # Parse the request
            subject, topic, grade_levels = self._parse_worksheet_request(user_message)
            
            # Generate worksheets for different grade levels
            worksheets = {}
            for grade in grade_levels:
                worksheets[grade] = self._create_worksheet(subject, topic, grade)
            
            # Format the response
            response = f"📚 **Differentiated Worksheets Generated**\n\n"
            response += f"**Subject:** {subject.title()}\n"
            response += f"**Topic:** {topic.title()}\n\n"
            
            for grade, worksheet in worksheets.items():
                response += f"**Grade {grade.split('_')[1]} Worksheet:**\n"
                response += f"{worksheet}\n\n"
                response += "---\n\n"
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't generate the worksheets. Error: {str(e)}"
    
    def _parse_worksheet_request(self, user_message: str) -> tuple:
        """Parse user message to extract subject, topic, and grade levels"""
        user_message_lower = user_message.lower()
        
        # Detect subject
        subject = 'mathematics'  # default
        for subj in self.subjects.keys():
            if subj in user_message_lower:
                subject = subj
                break
        
        # Detect topic
        topic = 'general'
        for subj, topics in self.subjects.items():
            if subj == subject:
                for t in topics:
                    if t in user_message_lower:
                        topic = t
                        break
                break
        
        # Detect grade levels (default to grades 3-5 for multi-grade)
        grade_levels = ['grade_3', 'grade_4', 'grade_5']
        for i in range(1, 11):
            if f'grade_{i}' in user_message_lower:
                grade_levels = [f'grade_{i}']
                break
        
        return subject, topic, grade_levels
    
    def _create_worksheet(self, subject: str, topic: str, grade_level: str) -> str:
        """Create a worksheet for a specific grade level"""
        grade_num = grade_level.split('_')[1]
        
        prompt = f"""
        Create a worksheet for {subject} topic "{topic}" for Grade {grade_num} students.
        
        Requirements:
        1. Age-appropriate content for Grade {grade_num}
        2. Clear instructions in simple language
        3. Mix of different question types (MCQ, fill in blanks, short answer)
        4. Include visual elements where helpful
        5. Progressive difficulty within the worksheet
        6. Include answer key
        7. Make it engaging and culturally relevant for Indian students
        8. Suitable for classroom use with limited resources
        
        Format the worksheet with:
        - Clear title
        - Instructions
        - Questions (numbered)
        - Space for answers
        - Answer key at the end
        
        Keep it concise but comprehensive.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def create_differentiated_materials(self, image_path: str, grade_levels: List[str], subject: str) -> str:
        """Create differentiated materials from uploaded textbook page"""
        try:
            # This would integrate with image analysis
            # For now, return a placeholder response
            response = f"📖 **Differentiated Materials from Textbook Page**\n\n"
            response += f"**Subject:** {subject.title()}\n"
            response += f"**Grade Levels:** {', '.join(grade_levels)}\n\n"
            
            for grade in grade_levels:
                grade_num = grade.split('_')[1]
                response += f"**Grade {grade_num} Version:**\n"
                response += f"- Simplified language and concepts\n"
                response += f"- More visual aids and examples\n"
                response += f"- Step-by-step instructions\n"
                response += f"- Additional practice problems\n\n"
            
            response += "📝 *Note: Full image analysis and worksheet generation will be implemented with OpenCV integration.*"
            
            return response
            
        except Exception as e:
            return f"Sorry, I couldn't process the textbook page. Error: {str(e)}"
    
    def get_supported_subjects(self) -> Dict[str, List[str]]:
        """Get list of supported subjects and topics"""
        return self.subjects
    
    def get_difficulty_levels(self) -> Dict[str, str]:
        """Get list of difficulty levels"""
        return self.difficulty_levels 