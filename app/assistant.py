import google.generativeai as genai
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List
from .content_generator import ContentGenerator
from .worksheet_generator import WorksheetGenerator
from .knowledge_base import KnowledgeBase
from .visual_aids import VisualAidsGenerator
from .lesson_planner import LessonPlanner

class SahayakAssistant:
    def __init__(self):
        """
        Initialize the Sahayak Teaching Assistant with Gemini AI
        """
        # Configure Gemini AI
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Load base prompt
        self.base_prompt = self._load_base_prompt()
        
        # Initialize teaching modules
        api_key = os.getenv('GEMINI_API_KEY')
        self.content_generator = ContentGenerator(api_key)
        self.worksheet_generator = WorksheetGenerator(api_key)
        self.knowledge_base = KnowledgeBase(api_key)
        self.visual_aids = VisualAidsGenerator(api_key)
        self.lesson_planner = LessonPlanner(api_key)
    
    def _load_base_prompt(self) -> str:
        """
        Load the base prompt for the teaching assistant
        """
        try:
            with open('prompts/base_prompt.txt', 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            return self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """
        Default prompt if base_prompt.txt is not found
        """
        return """
        You are Sahayak (सहायक), an AI teaching assistant designed to help teachers in multi-grade, low-resource classrooms across India.
        
        LANGUAGE PRIORITY: English (default) → Gujarati (ગુજરાતી) → Other Indian languages
        MAIN USERS: Gujarati-speaking teachers and students
        
        RESPONSE STYLE:
        - Give SHORT, CONCISE answers by default (2-3 sentences)
        - Only provide detailed/long answers when user specifically asks for:
          * "Give in detail"
          * "Explain thoroughly" 
          * "Generate a worksheet of X questions"
          * "Create a comprehensive lesson plan"
          * "Write a long story"
        
        Your role is to:
        1. Generate hyper-local content in Indian languages (Gujarati priority, then Hindi, Marathi, etc.)
        2. Create differentiated learning materials for different grade levels
        3. Provide instant knowledge support for student questions
        4. Generate visual aids and simple drawings for blackboard use
        5. Help with lesson planning and classroom management
        
        Guidelines:
        - Be supportive and encouraging to teachers
        - Provide culturally relevant content that connects with Indian students
        - Use simple, age-appropriate language for different grade levels
        - Include real-world examples from Indian context
        - Be mindful of limited resources in rural schools
        - Encourage inclusive and engaging teaching methods
        - Help teachers manage multi-grade classrooms effectively
        - When user asks in Gujarati, respond in Gujarati
        - Keep responses concise unless detailed explanation is requested
        
        Always respond in a helpful, conversational tone and provide practical teaching solutions.
        """
    
    def _handle_rate_limit(self, prompt: str, max_retries: int = 3) -> str:
        """
        Handle rate limiting with retry logic
        """
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                error_str = str(e)
                if "429" in error_str and "quota" in error_str.lower():
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 30  # Progressive backoff
                        print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return "I'm currently experiencing high demand. Please try again in a few minutes. This is a temporary issue with the AI service."
                else:
                    return f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}"
        
        return "I'm currently experiencing high demand. Please try again in a few minutes."
    
    def get_response(self, user_message: str, context: Dict[Any, Any] = None) -> str:
        """
        Get AI response based on user message and teaching context
        """
        try:
            # Check for specific teaching commands
            if self._is_content_generation_request(user_message):
                return self._handle_content_generation(user_message)
            
            elif self._is_worksheet_request(user_message):
                return self._handle_worksheet_generation(user_message)
            
            elif self._is_knowledge_request(user_message):
                return self._handle_knowledge_query(user_message)
            
            elif self._is_visual_aid_request(user_message):
                return self._handle_visual_aid_generation(user_message)
            
            elif self._is_lesson_planning_request(user_message):
                return self._handle_lesson_planning(user_message)
            
            else:
                # General teaching assistant response
                full_prompt = self._prepare_prompt(user_message, context or {})
                return self._handle_rate_limit(full_prompt)
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}"
    
    def _prepare_prompt(self, user_message: str, context: Dict[Any, Any]) -> str:
        """
        Prepare the complete prompt with teaching context and message
        """
        # Convert context to formatted string
        context_str = json.dumps(context, indent=2)
        
        # Current date for context
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        prompt = f"""
        {self.base_prompt}
        
        === TEACHING CONTEXT ===
        {context_str}
        
        === CURRENT DATE ===
        {current_date}
        
        === TEACHER'S QUESTION/MESSAGE ===
        {user_message}
        
        === CRITICAL INSTRUCTIONS ===
        IMPORTANT: You are helping a teacher in a multi-grade, low-resource classroom in India.
        
        LANGUAGE & RESPONSE GUIDELINES:
        - If user writes in Gujarati, respond in Gujarati
        - Default language: English, but prioritize Gujarati when appropriate
        - Keep responses SHORT and CONCISE (2-3 sentences) unless user specifically asks for detail
        - Only give long answers when user asks for: "detailed", "comprehensive", "thorough", "long", "many questions", etc.
        
        CONTENT GUIDELINES:
        - Provide culturally relevant content that connects with Indian students
        - Use simple, age-appropriate language for different grade levels
        - Include real-world examples from Indian context
        - Be mindful of limited resources in rural schools
        - Encourage inclusive and engaging teaching methods
        - Help teachers manage multi-grade classrooms effectively
        
        Please provide a helpful, practical response that empowers the teacher to deliver better education.
        """
        
        return prompt
    
    def _is_content_generation_request(self, user_message: str) -> bool:
        """Check if user wants to generate localized content"""
        content_keywords = [
            'create story', 'generate content', 'local language', 'gujarati', 'ગુજરાતી',
            'marathi', 'hindi', 'tamil', 'telugu', 'bengali', 'kannada', 'malayalam', 'punjabi',
            'story about', 'explain in', 'content in', 'કહાની', 'સમજાવો', 'વિષય'
        ]
        return any(keyword in user_message.lower() for keyword in content_keywords)
    
    def _is_worksheet_request(self, user_message: str) -> bool:
        """Check if user wants to generate worksheets"""
        worksheet_keywords = [
            'worksheet', 'differentiated', 'grade level', 'upload textbook', 'multiple versions',
            'tailored content', 'adaptive', 'difficulty level'
        ]
        return any(keyword in user_message.lower() for keyword in worksheet_keywords)
    
    def _is_knowledge_request(self, user_message: str) -> bool:
        """Check if user has a knowledge question"""
        knowledge_keywords = [
            'why is', 'how does', 'what is', 'explain', 'question', 'student asked',
            'knowledge', 'answer', 'clarify'
        ]
        return any(keyword in user_message.lower() for keyword in knowledge_keywords)
    
    def _is_visual_aid_request(self, user_message: str) -> bool:
        """Check if user wants visual aids"""
        visual_keywords = [
            'drawing', 'chart', 'diagram', 'visual aid', 'blackboard', 'picture',
            'illustration', 'graph', 'sketch'
        ]
        return any(keyword in user_message.lower() for keyword in visual_keywords)
    
    def _is_lesson_planning_request(self, user_message: str) -> bool:
        """Check if user wants lesson planning help"""
        planning_keywords = [
            'lesson plan', 'weekly plan', 'classroom management', 'activity',
            'schedule', 'curriculum', 'teaching plan'
        ]
        return any(keyword in user_message.lower() for keyword in planning_keywords)
    
    def _handle_content_generation(self, user_message: str) -> str:
        """Handle localized content generation requests"""
        try:
            # Check if user wants detailed content
            wants_detailed = any(word in user_message.lower() for word in 
                               ['detailed', 'comprehensive', 'thorough', 'long', 'many', 'extensive'])
            
            # Extract parameters from user message
            # This is a simplified approach - in production, use NLP to extract parameters
            result = self.content_generator.generate_story(
                subject="General",
                topic="Educational Content",
                grade="5-8",
                language="English",
                story_type="educational"
            )
            
            if wants_detailed:
                return f"Generated detailed content successfully! Here's the complete content:\n\n{result}"
            else:
                # Return a concise summary
                return f"Content generated! Here's a brief version:\n\n{result[:200]}..." if len(result) > 200 else result
                
        except Exception as e:
            return f"Sorry, I couldn't generate the content. Error: {str(e)}"
    
    def _handle_worksheet_generation(self, user_message: str) -> str:
        """Handle worksheet generation requests"""
        try:
            # Check if user wants detailed/many questions
            wants_detailed = any(word in user_message.lower() for word in 
                               ['detailed', 'comprehensive', 'thorough', 'long', 'many', 'extensive', '100', '50'])
            
            result = self.worksheet_generator.generate_worksheet(
                subject="Math",
                topic="Basic Operations",
                grade="5",
                difficulty="medium",
                language="English"
            )
            
            if wants_detailed:
                return f"Detailed worksheet generated successfully!\n\n{result}"
            else:
                # Return a concise summary
                return f"Worksheet created! Here's a brief version:\n\n{result[:300]}..." if len(result) > 300 else result
                
        except Exception as e:
            return f"Sorry, I couldn't generate the worksheets. Error: {str(e)}"
    
    def _handle_knowledge_query(self, user_message: str) -> str:
        """Handle knowledge base queries"""
        try:
            result = self.knowledge_base.get_answer(user_message)
            return result
        except Exception as e:
            return f"Sorry, I couldn't find an answer. Error: {str(e)}"
    
    def _handle_visual_aid_generation(self, user_message: str) -> str:
        """Handle visual aid generation requests"""
        try:
            result = self.visual_aids.generate_educational_image(
                subject="Science",
                topic="Basic Concepts",
                grade="5",
                language="English"
            )
            return f"Visual aid generated successfully! {result.get('metadata', {})}"
        except Exception as e:
            return f"Sorry, I couldn't generate the visual aid. Error: {str(e)}"
    
    def _handle_lesson_planning(self, user_message: str) -> str:
        """Handle lesson planning requests"""
        try:
            result = self.lesson_planner.generate_lesson_plan(
                subject="Science",
                topic="Basic Concepts",
                grade="5",
                duration="45 minutes",
                language="English"
            )
            return f"Lesson plan created successfully! {result.get('metadata', {})}"
        except Exception as e:
            return f"Sorry, I couldn't create the lesson plan. Error: {str(e)}"
