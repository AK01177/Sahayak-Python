"""
Data loader for Sahayak - AI Teaching Assistant
Handles loading and processing of educational content and knowledge base
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

class DataLoader:
    """Handles loading and processing of Sahayak's educational data"""
    
    def __init__(self, data_file: str = 'data/personal_data.json'):
        self.data_file = data_file
        self.logger = logging.getLogger(__name__)
        
    def load_data(self) -> Dict[str, Any]:
        """Load educational data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            self.logger.error(f"Data file not found: {self.data_file}")
            return self._create_default_data()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in data file: {e}")
            return self._create_default_data()
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            return self._create_default_data()
    
    def _create_default_data(self) -> Dict[str, Any]:
        """Create default educational data structure"""
        return {
            "profile": {
                "name": "Sahayak",
                "type": "AI Teaching Assistant",
                "purpose": "Multi-grade Indian classroom support",
                "languages": ["English", "Hindi", "Gujarati", "Marathi", "Bengali", "Tamil", "Telugu", "Kannada", "Malayalam"],
                "subjects": ["Mathematics", "Science", "English", "Hindi", "Social Studies", "Computer Science"],
                "grade_levels": ["Class 1-5", "Class 6-8", "Class 9-10", "Class 11-12"],
                "curriculum": "CBSE, ICSE, State Boards"
            },
            "content_generation": {
                "subjects": {},
                "languages": {}
            },
            "worksheet_generation": {
                "types": {}
            },
            "lesson_planning": {
                "components": {}
            },
            "student_support": {
                "question_types": {},
                "response_style": {}
            },
            "visual_aids": {
                "types": {},
                "features": {}
            },
            "knowledge_base": {
                "subjects": {},
                "teaching_methods": {}
            },
            "capabilities": {},
            "usage_context": {
                "target_users": [],
                "use_cases": [],
                "benefits": []
            },
            "project_context": {
                "purpose": "AI-powered educational assistant for Indian classrooms",
                "focus": "Multi-grade, multi-language, multi-subject support",
                "target_audience": "Indian students and teachers",
                "curriculum_alignment": "CBSE, ICSE, and State Board curricula",
                "last_updated": datetime.now().strftime("%Y-%m-%d")
            }
        }
    
    def get_subject_data(self, subject: str) -> Dict[str, Any]:
        """Get data for a specific subject"""
        data = self.load_data()
        return data.get('content_generation', {}).get('subjects', {}).get(subject, {})
    
    def get_language_data(self, language: str) -> Dict[str, Any]:
        """Get data for a specific language"""
        data = self.load_data()
        return data.get('content_generation', {}).get('languages', {}).get(language, {})
    
    def get_worksheet_types(self) -> Dict[str, Any]:
        """Get available worksheet types"""
        data = self.load_data()
        return data.get('worksheet_generation', {}).get('types', {})
    
    def get_lesson_components(self) -> Dict[str, Any]:
        """Get lesson planning components"""
        data = self.load_data()
        return data.get('lesson_planning', {}).get('components', {})
    
    def get_knowledge_base(self, subject: Optional[str] = None) -> Dict[str, Any]:
        """Get knowledge base data for a subject or all subjects"""
        data = self.load_data()
        knowledge_base = data.get('knowledge_base', {}).get('subjects', {})
        
        if subject:
            return knowledge_base.get(subject, {})
        return knowledge_base
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get Sahayak's capabilities"""
        data = self.load_data()
        return data.get('capabilities', {})
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        data = self.load_data()
        return data.get('profile', {}).get('languages', [])
    
    def get_supported_subjects(self) -> List[str]:
        """Get list of supported subjects"""
        data = self.load_data()
        return data.get('profile', {}).get('subjects', [])
    
    def get_grade_levels(self) -> List[str]:
        """Get list of supported grade levels"""
        data = self.load_data()
        return data.get('profile', {}).get('grade_levels', [])
    
    def get_content_insights(self) -> Dict[str, Any]:
        """Get insights about available content"""
        data = self.load_data()
        
        content_generation = data.get('content_generation', {})
        subjects = content_generation.get('subjects', {})
        languages = content_generation.get('languages', {})
        
        insights = {
            'total_subjects': len(subjects),
            'total_languages': len(languages),
            'subjects': list(subjects.keys()),
            'languages': list(languages.keys()),
            'content_types': set(),
            'difficulty_levels': set(),
            'topics_count': 0
        }
        
        # Analyze subjects
        for subject_data in subjects.values():
            insights['content_types'].update(subject_data.get('content_types', []))
            insights['difficulty_levels'].update(subject_data.get('difficulty_levels', []))
            insights['topics_count'] += len(subject_data.get('topics', []))
        
        insights['content_types'] = list(insights['content_types'])
        insights['difficulty_levels'] = list(insights['difficulty_levels'])
        
        return insights
    
    def get_usage_context(self) -> Dict[str, Any]:
        """Get usage context information"""
        data = self.load_data()
        return data.get('usage_context', {})
    
    def get_project_context(self) -> Dict[str, Any]:
        """Get project context information"""
        data = self.load_data()
        return data.get('project_context', {})
    
    def validate_data_structure(self, data: Dict[str, Any]) -> bool:
        """Validate that data has required structure"""
        required_keys = ['profile', 'content_generation', 'worksheet_generation', 
                        'lesson_planning', 'student_support', 'visual_aids', 
                        'knowledge_base', 'capabilities', 'usage_context', 'project_context']
        
        for key in required_keys:
            if key not in data:
                self.logger.error(f"Missing required key: {key}")
                return False
        
        return True
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get a summary of the current data"""
        data = self.load_data()
        
        summary = {
            'profile': {
                'name': data.get('profile', {}).get('name', 'Unknown'),
                'type': data.get('profile', {}).get('type', 'Unknown'),
                'languages_count': len(data.get('profile', {}).get('languages', [])),
                'subjects_count': len(data.get('profile', {}).get('subjects', [])),
                'grade_levels_count': len(data.get('profile', {}).get('grade_levels', []))
            },
            'content_generation': {
                'subjects_count': len(data.get('content_generation', {}).get('subjects', {})),
                'languages_count': len(data.get('content_generation', {}).get('languages', {}))
            },
            'worksheet_generation': {
                'types_count': len(data.get('worksheet_generation', {}).get('types', {}))
            },
            'lesson_planning': {
                'components_count': len(data.get('lesson_planning', {}).get('components', {}))
            },
            'knowledge_base': {
                'subjects_count': len(data.get('knowledge_base', {}).get('subjects', {}))
            },
            'capabilities_count': len(data.get('capabilities', {})),
            'last_updated': data.get('project_context', {}).get('last_updated', 'Unknown')
        }
        
        return summary
    
    def backup_data(self, backup_dir: str = 'data/backups') -> str:
        """Create a backup of the current data"""
        try:
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{backup_dir}/sahayak_data_backup_{timestamp}.json"
            
            data = self.load_data()
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data backed up to: {backup_file}")
            return backup_file
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return ""
    
    def restore_data(self, backup_file: str) -> bool:
        """Restore data from a backup file"""
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if self.validate_data_structure(data):
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"Data restored from: {backup_file}")
                return True
            else:
                self.logger.error("Backup file has invalid structure")
                return False
        except Exception as e:
            self.logger.error(f"Error restoring data: {e}")
            return False
