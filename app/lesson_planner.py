"""
Lesson Planner for Sahayak AI Teaching Assistant
Generates comprehensive lesson plans for multi-grade Indian classrooms
"""

import json
import datetime
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai

class LessonPlanner:
    def __init__(self, api_key: str):
        """Initialize the lesson planner with Google AI"""
        if not api_key or api_key == 'test_key':
            self.model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini model: {e}")
            self.model = None
        
    def generate_lesson_plan(self, subject: str, topic: str, grade: str, 
                           duration: str = "45 minutes", language: str = "English",
                           learning_objectives: List[str] = None,
                           prerequisites: List[str] = None) -> Dict:
        """
        Generate a comprehensive lesson plan for Indian classrooms
        
        Args:
            subject: Subject (Math, Science, English, Hindi, etc.)
            topic: Specific topic to teach
            grade: Grade level (1-12)
            duration: Lesson duration (e.g., "45 minutes", "1 hour")
            language: Primary language of instruction
            learning_objectives: List of specific learning objectives
            prerequisites: List of prerequisite knowledge
            
        Returns:
            Dict with complete lesson plan
        """
        try:
            if not self.model:
                return {
                    "success": False,
                    "error": "API key not valid. Please pass a valid API key.",
                    "metadata": {
                        "subject": subject,
                        "topic": topic,
                        "grade": grade
                    }
                }
            
            # Create detailed lesson plan prompt
            prompt = self._create_lesson_plan_prompt(
                subject, topic, grade, duration, language, 
                learning_objectives, prerequisites
            )
            
            # Generate lesson plan using AI
            response = self.model.generate_content(prompt)
            lesson_plan = self._parse_lesson_plan_response(response.text)
            
            return {
                "success": True,
                "lesson_plan": lesson_plan,
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grade": grade,
                    "duration": duration,
                    "language": language,
                    "generated_at": datetime.datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grade": grade
                }
            }
    
    def create_weekly_plan(self, subject: str, grade: str, week_number: int,
                          topics: List[str], language: str = "English") -> Dict:
        """
        Generate a weekly lesson plan
        
        Args:
            subject: Subject to plan for
            grade: Grade level
            week_number: Week number in academic year
            topics: List of topics for the week
            language: Language of instruction
            
        Returns:
            Dict with weekly plan
        """
        try:
            prompt = self._create_weekly_plan_prompt(
                subject, grade, week_number, topics, language
            )
            
            response = self.model.generate_content(prompt)
            weekly_plan = self._parse_weekly_plan_response(response.text)
            
            return {
                "success": True,
                "weekly_plan": weekly_plan,
                "metadata": {
                    "subject": subject,
                    "grade": grade,
                    "week_number": week_number,
                    "language": language,
                    "topics_count": len(topics)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "subject": subject,
                    "grade": grade,
                    "week_number": week_number
                }
            }
    
    def generate_assessment_plan(self, subject: str, topic: str, grade: str,
                               assessment_type: str = "formative",
                               language: str = "English") -> Dict:
        """
        Generate assessment strategies and tools
        
        Args:
            subject: Subject being assessed
            topic: Topic being assessed
            grade: Grade level
            assessment_type: Type of assessment (formative, summative, diagnostic)
            language: Language for assessment
            
        Returns:
            Dict with assessment plan
        """
        try:
            prompt = self._create_assessment_prompt(
                subject, topic, grade, assessment_type, language
            )
            
            response = self.model.generate_content(prompt)
            assessment_plan = self._parse_assessment_response(response.text)
            
            return {
                "success": True,
                "assessment_plan": assessment_plan,
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grade": grade,
                    "assessment_type": assessment_type,
                    "language": language
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grade": grade
                }
            }
    
    def create_differentiated_plan(self, subject: str, topic: str, grade: str,
                                 student_profiles: List[Dict],
                                 language: str = "English") -> Dict:
        """
        Create differentiated lesson plans for diverse learners
        
        Args:
            subject: Subject to teach
            topic: Topic to cover
            grade: Grade level
            student_profiles: List of student profiles with learning needs
            language: Language of instruction
            
        Returns:
            Dict with differentiated plans
        """
        try:
            prompt = self._create_differentiated_prompt(
                subject, topic, grade, student_profiles, language
            )
            
            response = self.model.generate_content(prompt)
            differentiated_plans = self._parse_differentiated_response(response.text)
            
            return {
                "success": True,
                "differentiated_plans": differentiated_plans,
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grade": grade,
                    "language": language,
                    "student_count": len(student_profiles)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grade": grade
                }
            }
    
    def _create_lesson_plan_prompt(self, subject: str, topic: str, grade: str,
                                 duration: str, language: str,
                                 learning_objectives: List[str],
                                 prerequisites: List[str]) -> str:
        """Create detailed prompt for lesson plan generation"""
        
        grade_context = {
            "1-3": "Primary level with focus on basic concepts, hands-on activities, and simple explanations",
            "4-6": "Upper primary with more structured learning, introduction to complex concepts",
            "7-9": "Middle school with analytical thinking, practical applications",
            "10-12": "Secondary level with advanced concepts, critical thinking, and exam preparation"
        }
        
        language_context = {
            "Hindi": "Use Hindi for explanations and examples where appropriate",
            "Marathi": "Use Marathi for explanations and examples where appropriate",
            "Tamil": "Use Tamil for explanations and examples where appropriate",
            "Telugu": "Use Telugu for explanations and examples where appropriate",
            "Bengali": "Use Bengali for explanations and examples where appropriate",
            "English": "Use clear English with simple vocabulary"
        }
        
        objectives_text = ""
        if learning_objectives:
            objectives_text = "\nSpecific Learning Objectives:\n" + "\n".join([f"- {obj}" for obj in learning_objectives])
        
        prerequisites_text = ""
        if prerequisites:
            prerequisites_text = "\nPrerequisites:\n" + "\n".join([f"- {pre}" for pre in prerequisites])
        
        prompt = f"""
        Create a comprehensive lesson plan for {subject} topic: {topic}
        
        Context:
        - Grade Level: {grade} ({grade_context.get(grade, 'Appropriate complexity')})
        - Duration: {duration}
        - Language: {language} ({language_context.get(language, 'Clear instruction')})
        - Subject: {subject}
        
        {objectives_text}
        {prerequisites_text}
        
        Requirements for Indian Classroom Context:
        1. Include culturally relevant examples and contexts
        2. Consider diverse learning styles and abilities
        3. Include hands-on activities suitable for available resources
        4. Provide clear assessment criteria
        5. Include time management for each activity
        6. Consider classroom management strategies
        7. Include differentiation strategies for mixed-ability classes
        
        Structure the lesson plan with:
        1. Lesson Overview and Objectives
        2. Prerequisites and Prior Knowledge
        3. Materials and Resources Required
        4. Detailed Lesson Procedure (with time allocation)
        5. Assessment and Evaluation Methods
        6. Homework/Extension Activities
        7. Reflection and Notes for Future Lessons
        
        Make the plan practical, engaging, and suitable for Indian classroom realities.
        """
        
        return prompt
    
    def _create_weekly_plan_prompt(self, subject: str, grade: str, week_number: int,
                                 topics: List[str], language: str) -> str:
        """Create prompt for weekly lesson planning"""
        
        topics_text = "\n".join([f"- {topic}" for topic in topics])
        
        prompt = f"""
        Create a comprehensive weekly lesson plan for {subject} (Grade {grade}, Week {week_number})
        
        Topics to cover this week:
        {topics_text}
        
        Language of instruction: {language}
        
        Requirements:
        1. Daily lesson breakdown with time allocation
        2. Learning objectives for each day
        3. Activities and teaching strategies
        4. Assessment methods for each topic
        5. Homework assignments
        6. Resources and materials needed
        7. Differentiation strategies for diverse learners
        8. Integration with other subjects where relevant
        
        Consider:
        - Indian educational context and curriculum
        - Available resources and infrastructure
        - Student diversity and learning needs
        - Assessment and evaluation methods
        - Parent involvement and communication
        
        Structure the weekly plan with:
        1. Weekly Overview and Goals
        2. Daily Lesson Plans (Monday to Friday)
        3. Assessment Schedule
        4. Resource Requirements
        5. Notes for Teachers
        """
        
        return prompt
    
    def _create_assessment_prompt(self, subject: str, topic: str, grade: str,
                                assessment_type: str, language: str) -> str:
        """Create prompt for assessment planning"""
        
        assessment_context = {
            "formative": "Ongoing assessment during learning to provide feedback and guide instruction",
            "summative": "End-of-unit/topic assessment to evaluate learning outcomes",
            "diagnostic": "Assessment to identify student strengths, weaknesses, and learning gaps"
        }
        
        prompt = f"""
        Create an assessment plan for {subject} topic: {topic} (Grade {grade})
        
        Assessment Type: {assessment_type} ({assessment_context.get(assessment_type, 'Comprehensive evaluation')})
        Language: {language}
        
        Requirements:
        1. Assessment objectives and criteria
        2. Multiple assessment methods and tools
        3. Rubrics and evaluation criteria
        4. Accommodations for diverse learners
        5. Feedback strategies
        6. Remediation plans for struggling students
        7. Extension activities for advanced learners
        
        Include:
        - Written assessments (MCQ, short answer, essay)
        - Oral assessments and presentations
        - Practical/hands-on assessments
        - Project-based assessments
        - Peer and self-assessment methods
        - Technology-based assessment tools
        
        Consider Indian educational context:
        - Large class sizes
        - Limited resources
        - Diverse student backgrounds
        - Language barriers
        - Parent expectations
        
        Structure the assessment plan with:
        1. Assessment Overview and Objectives
        2. Assessment Methods and Tools
        3. Evaluation Criteria and Rubrics
        4. Implementation Timeline
        5. Feedback and Remediation Strategies
        6. Reporting and Communication Plan
        """
        
        return prompt
    
    def _create_differentiated_prompt(self, subject: str, topic: str, grade: str,
                                    student_profiles: List[Dict], language: str) -> str:
        """Create prompt for differentiated lesson planning"""
        
        profiles_text = ""
        for i, profile in enumerate(student_profiles):
            profiles_text += f"\nStudent {i+1}:\n"
            for key, value in profile.items():
                profiles_text += f"- {key}: {value}\n"
        
        prompt = f"""
        Create differentiated lesson plans for {subject} topic: {topic} (Grade {grade})
        
        Language of instruction: {language}
        
        Student Profiles:
        {profiles_text}
        
        Requirements:
        1. Individualized learning objectives for each student
        2. Modified activities and materials
        3. Differentiated assessment methods
        4. Accommodations and modifications
        5. Support strategies for struggling learners
        6. Extension activities for advanced learners
        7. Grouping strategies for collaborative learning
        
        Consider:
        - Learning disabilities and special needs
        - Language barriers and multilingual support
        - Different learning styles (visual, auditory, kinesthetic)
        - Socioeconomic and cultural factors
        - Technology access and digital literacy
        - Parent involvement and support
        
        Structure the differentiated plans with:
        1. Overview of Differentiation Strategy
        2. Individual Student Plans
        3. Group Activities and Collaboration
        4. Assessment Modifications
        5. Support and Resources
        6. Monitoring and Progress Tracking
        """
        
        return prompt
    
    def _parse_lesson_plan_response(self, response_text: str) -> Dict:
        """Parse AI response into structured lesson plan"""
        try:
            # Try to extract structured content from response
            sections = {
                "overview": "",
                "objectives": [],
                "prerequisites": [],
                "materials": [],
                "procedure": [],
                "assessment": [],
                "homework": [],
                "reflection": ""
            }
            
            # Simple parsing - in production, use more sophisticated NLP
            lines = response_text.split('\n')
            current_section = "overview"
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Detect section headers
                if any(keyword in line.lower() for keyword in ["objective", "goal", "aim"]):
                    current_section = "objectives"
                elif any(keyword in line.lower() for keyword in ["prerequisite", "prior knowledge", "background"]):
                    current_section = "prerequisites"
                elif any(keyword in line.lower() for keyword in ["material", "resource", "equipment"]):
                    current_section = "materials"
                elif any(keyword in line.lower() for keyword in ["procedure", "method", "activity", "step"]):
                    current_section = "procedure"
                elif any(keyword in line.lower() for keyword in ["assessment", "evaluation", "test"]):
                    current_section = "assessment"
                elif any(keyword in line.lower() for keyword in ["homework", "assignment", "extension"]):
                    current_section = "homework"
                elif any(keyword in line.lower() for keyword in ["reflection", "note", "future"]):
                    current_section = "reflection"
                else:
                    # Add content to current section
                    if current_section in ["objectives", "prerequisites", "materials", "procedure", "assessment", "homework"]:
                        if line.startswith('-') or line.startswith('•'):
                            sections[current_section].append(line[1:].strip())
                        else:
                            sections[current_section].append(line)
                    else:
                        sections[current_section] += line + "\n"
            
            return sections
            
        except Exception as e:
            # Fallback to simple text structure
            return {
                "raw_content": response_text,
                "parsed": False,
                "error": str(e)
            }
    
    def _parse_weekly_plan_response(self, response_text: str) -> Dict:
        """Parse AI response into structured weekly plan"""
        try:
            # Extract daily plans and other sections
            sections = {
                "overview": "",
                "daily_plans": {},
                "assessment_schedule": [],
                "resources": [],
                "teacher_notes": ""
            }
            
            lines = response_text.split('\n')
            current_section = "overview"
            current_day = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect sections
                if any(day in line.lower() for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]):
                    current_section = "daily_plans"
                    current_day = line.split()[0].title()
                    sections["daily_plans"][current_day] = []
                elif any(keyword in line.lower() for keyword in ["assessment", "evaluation", "test"]):
                    current_section = "assessment_schedule"
                elif any(keyword in line.lower() for keyword in ["resource", "material", "equipment"]):
                    current_section = "resources"
                elif any(keyword in line.lower() for keyword in ["note", "reflection", "teacher"]):
                    current_section = "teacher_notes"
                else:
                    # Add content to appropriate section
                    if current_section == "daily_plans" and current_day:
                        sections["daily_plans"][current_day].append(line)
                    elif current_section in ["assessment_schedule", "resources"]:
                        if line.startswith('-') or line.startswith('•'):
                            sections[current_section].append(line[1:].strip())
                        else:
                            sections[current_section].append(line)
                    else:
                        sections[current_section] += line + "\n"
            
            return sections
            
        except Exception as e:
            return {
                "raw_content": response_text,
                "parsed": False,
                "error": str(e)
            }
    
    def _parse_assessment_response(self, response_text: str) -> Dict:
        """Parse AI response into structured assessment plan"""
        try:
            sections = {
                "overview": "",
                "methods": [],
                "criteria": [],
                "timeline": [],
                "feedback": [],
                "reporting": ""
            }
            
            lines = response_text.split('\n')
            current_section = "overview"
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect sections
                if any(keyword in line.lower() for keyword in ["method", "tool", "technique"]):
                    current_section = "methods"
                elif any(keyword in line.lower() for keyword in ["criteria", "rubric", "standard"]):
                    current_section = "criteria"
                elif any(keyword in line.lower() for keyword in ["timeline", "schedule", "date"]):
                    current_section = "timeline"
                elif any(keyword in line.lower() for keyword in ["feedback", "remediation", "support"]):
                    current_section = "feedback"
                elif any(keyword in line.lower() for keyword in ["report", "communication", "parent"]):
                    current_section = "reporting"
                else:
                    # Add content to current section
                    if current_section in ["methods", "criteria", "timeline", "feedback"]:
                        if line.startswith('-') or line.startswith('•'):
                            sections[current_section].append(line[1:].strip())
                        else:
                            sections[current_section].append(line)
                    else:
                        sections[current_section] += line + "\n"
            
            return sections
            
        except Exception as e:
            return {
                "raw_content": response_text,
                "parsed": False,
                "error": str(e)
            }
    
    def _parse_differentiated_response(self, response_text: str) -> Dict:
        """Parse AI response into structured differentiated plans"""
        try:
            sections = {
                "overview": "",
                "individual_plans": {},
                "group_activities": [],
                "assessment_modifications": [],
                "support_resources": [],
                "progress_tracking": ""
            }
            
            lines = response_text.split('\n')
            current_section = "overview"
            current_student = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect sections
                if any(keyword in line.lower() for keyword in ["student", "individual", "learner"]):
                    current_section = "individual_plans"
                    # Try to extract student identifier
                    if "student" in line.lower():
                        current_student = line.split()[0] if line.split() else f"Student_{len(sections['individual_plans']) + 1}"
                        sections["individual_plans"][current_student] = []
                elif any(keyword in line.lower() for keyword in ["group", "collaboration", "team"]):
                    current_section = "group_activities"
                elif any(keyword in line.lower() for keyword in ["assessment", "evaluation", "modification"]):
                    current_section = "assessment_modifications"
                elif any(keyword in line.lower() for keyword in ["support", "resource", "accommodation"]):
                    current_section = "support_resources"
                elif any(keyword in line.lower() for keyword in ["progress", "tracking", "monitoring"]):
                    current_section = "progress_tracking"
                else:
                    # Add content to appropriate section
                    if current_section == "individual_plans" and current_student:
                        sections["individual_plans"][current_student].append(line)
                    elif current_section in ["group_activities", "assessment_modifications", "support_resources"]:
                        if line.startswith('-') or line.startswith('•'):
                            sections[current_section].append(line[1:].strip())
                        else:
                            sections[current_section].append(line)
                    else:
                        sections[current_section] += line + "\n"
            
            return sections
            
        except Exception as e:
            return {
                "raw_content": response_text,
                "parsed": False,
                "error": str(e)
            } 