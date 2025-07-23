"""
Data updater for Sahayak - AI Teaching Assistant
Handles updates to educational content and knowledge base
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.data_loader import DataLoader

class DataUpdater:
    """Handles updates to Sahayak's educational data"""
    
    def __init__(self, data_file: str = 'data/personal_data.json'):
        self.data_file = data_file
        self.data_loader = DataLoader(data_file)
        
    def load_data(self) -> Dict[str, Any]:
        """Load current data"""
        return self.data_loader.load_data()
    
    def save_data(self, data: Dict[str, Any]) -> None:
        """Save data with backup"""
        self._create_backup()
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _create_backup(self) -> None:
        """Create backup of current data"""
        if not os.path.exists(self.data_file):
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = 'data/backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_file = f"{backup_dir}/sahayak_data_backup_{timestamp}.json"
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def update_subject_content(self, subject: str, updates: Dict[str, Any]) -> List[str]:
        """Update content for a specific subject"""
        data = self.load_data()
        changes_made = []
        
        if 'content_generation' not in data:
            data['content_generation'] = {'subjects': {}}
        
        if 'subjects' not in data['content_generation']:
            data['content_generation']['subjects'] = {}
        
        if subject not in data['content_generation']['subjects']:
            data['content_generation']['subjects'][subject] = {
                'topics': [],
                'difficulty_levels': [],
                'content_types': []
            }
        
        subject_data = data['content_generation']['subjects'][subject]
        
        # Update topics
        if 'topics' in updates:
            old_topics = subject_data.get('topics', [])
            new_topics = updates['topics']
            subject_data['topics'] = new_topics
            changes_made.append(f"Updated {subject} topics: {len(old_topics)} → {len(new_topics)} topics")
        
        # Update difficulty levels
        if 'difficulty_levels' in updates:
            old_levels = subject_data.get('difficulty_levels', [])
            new_levels = updates['difficulty_levels']
            subject_data['difficulty_levels'] = new_levels
            changes_made.append(f"Updated {subject} difficulty levels: {old_levels} → {new_levels}")
        
        # Update content types
        if 'content_types' in updates:
            old_types = subject_data.get('content_types', [])
            new_types = updates['content_types']
            subject_data['content_types'] = new_types
            changes_made.append(f"Updated {subject} content types: {old_types} → {new_types}")
        
        self.save_data(data)
        return changes_made
    
    def update_language_support(self, language: str, updates: Dict[str, Any]) -> List[str]:
        """Update language support settings"""
        data = self.load_data()
        changes_made = []
        
        if 'content_generation' not in data:
            data['content_generation'] = {'languages': {}}
        
        if 'languages' not in data['content_generation']:
            data['content_generation']['languages'] = {}
        
        if language not in data['content_generation']['languages']:
            data['content_generation']['languages'][language] = {
                'proficiency': 'Good',
                'content_style': 'Clear and engaging'
            }
        
        language_data = data['content_generation']['languages'][language]
        
        # Update proficiency
        if 'proficiency' in updates:
            old_proficiency = language_data.get('proficiency', 'Good')
            new_proficiency = updates['proficiency']
            language_data['proficiency'] = new_proficiency
            changes_made.append(f"Updated {language} proficiency: {old_proficiency} → {new_proficiency}")
        
        # Update content style
        if 'content_style' in updates:
            old_style = language_data.get('content_style', 'Clear and engaging')
            new_style = updates['content_style']
            language_data['content_style'] = new_style
            changes_made.append(f"Updated {language} content style: {old_style} → {new_style}")
        
        self.save_data(data)
        return changes_made
    
    def update_worksheet_types(self, worksheet_type: str, updates: Dict[str, Any]) -> List[str]:
        """Update worksheet generation types"""
        data = self.load_data()
        changes_made = []
        
        if 'worksheet_generation' not in data:
            data['worksheet_generation'] = {'types': {}}
        
        if 'types' not in data['worksheet_generation']:
            data['worksheet_generation']['types'] = {}
        
        if worksheet_type not in data['worksheet_generation']['types']:
            data['worksheet_generation']['types'][worksheet_type] = {
                'description': '',
                'difficulty_levels': [],
                'subjects': []
            }
        
        worksheet_data = data['worksheet_generation']['types'][worksheet_type]
        
        # Update description
        if 'description' in updates:
            old_desc = worksheet_data.get('description', '')
            new_desc = updates['description']
            worksheet_data['description'] = new_desc
            changes_made.append(f"Updated {worksheet_type} description: {old_desc} → {new_desc}")
        
        # Update difficulty levels
        if 'difficulty_levels' in updates:
            old_levels = worksheet_data.get('difficulty_levels', [])
            new_levels = updates['difficulty_levels']
            worksheet_data['difficulty_levels'] = new_levels
            changes_made.append(f"Updated {worksheet_type} difficulty levels: {old_levels} → {new_levels}")
        
        # Update subjects
        if 'subjects' in updates:
            old_subjects = worksheet_data.get('subjects', [])
            new_subjects = updates['subjects']
            worksheet_data['subjects'] = new_subjects
            changes_made.append(f"Updated {worksheet_type} subjects: {old_subjects} → {new_subjects}")
        
        self.save_data(data)
        return changes_made
    
    def update_lesson_planning(self, component: str, updates: Dict[str, Any]) -> List[str]:
        """Update lesson planning components"""
        data = self.load_data()
        changes_made = []
        
        if 'lesson_planning' not in data:
            data['lesson_planning'] = {'components': {}}
        
        if 'components' not in data['lesson_planning']:
            data['lesson_planning']['components'] = {}
        
        if component not in data['lesson_planning']['components']:
            data['lesson_planning']['components'][component] = {
                'description': '',
                'types': []
            }
        
        component_data = data['lesson_planning']['components'][component]
        
        # Update description
        if 'description' in updates:
            old_desc = component_data.get('description', '')
            new_desc = updates['description']
            component_data['description'] = new_desc
            changes_made.append(f"Updated {component} description: {old_desc} → {new_desc}")
        
        # Update types
        if 'types' in updates:
            old_types = component_data.get('types', [])
            new_types = updates['types']
            component_data['types'] = new_types
            changes_made.append(f"Updated {component} types: {old_types} → {new_types}")
        
        self.save_data(data)
        return changes_made
    
    def update_capabilities(self, capability: str, enabled: bool) -> List[str]:
        """Update Sahayak's capabilities"""
        data = self.load_data()
        changes_made = []
        
        if 'capabilities' not in data:
            data['capabilities'] = {}
        
        if capability not in data['capabilities']:
            data['capabilities'][capability] = False
        
        old_status = data['capabilities'][capability]
        data['capabilities'][capability] = enabled
        
        status_text = "enabled" if enabled else "disabled"
        changes_made.append(f"{capability} capability {status_text}: {old_status} → {enabled}")
        
        self.save_data(data)
        return changes_made
    
    def add_knowledge_base_entry(self, subject: str, topic: str, content: Dict[str, Any]) -> List[str]:
        """Add new knowledge base entry"""
        data = self.load_data()
        changes_made = []
        
        if 'knowledge_base' not in data:
            data['knowledge_base'] = {'subjects': {}}
        
        if 'subjects' not in data['knowledge_base']:
            data['knowledge_base']['subjects'] = {}
        
        if subject not in data['knowledge_base']['subjects']:
            data['knowledge_base']['subjects'][subject] = {
                'topics': {},
                'grade_levels': [],
                'resources': []
            }
        
        subject_data = data['knowledge_base']['subjects'][subject]
        
        if 'topics' not in subject_data:
            subject_data['topics'] = {}
        
        # Add new topic
        if topic not in subject_data['topics']:
            subject_data['topics'][topic] = content
            changes_made.append(f"Added new topic '{topic}' to {subject} knowledge base")
        else:
            # Update existing topic
            old_content = subject_data['topics'][topic]
            subject_data['topics'][topic] = content
            changes_made.append(f"Updated topic '{topic}' in {subject} knowledge base")
        
        self.save_data(data)
        return changes_made
    
    def update_project_context(self, updates: Dict[str, Any]) -> List[str]:
        """Update project context information"""
        data = self.load_data()
        changes_made = []
        
        if 'project_context' not in data:
            data['project_context'] = {}
        
        for key, value in updates.items():
            old_value = data['project_context'].get(key, 'Not set')
            data['project_context'][key] = value
            changes_made.append(f"Updated {key}: {old_value} → {value}")
        
        # Always update last_updated timestamp
        data['project_context']['last_updated'] = datetime.now().strftime("%Y-%m-%d")
        
        self.save_data(data)
        return changes_made
    
    def get_update_summary(self) -> Dict[str, Any]:
        """Get summary of current data structure"""
        data = self.load_data()
        
        summary = {
            'total_subjects': len(data.get('content_generation', {}).get('subjects', {})),
            'total_languages': len(data.get('content_generation', {}).get('languages', {})),
            'worksheet_types': len(data.get('worksheet_generation', {}).get('types', {})),
            'lesson_components': len(data.get('lesson_planning', {}).get('components', {})),
            'capabilities': len(data.get('capabilities', {})),
            'knowledge_base_subjects': len(data.get('knowledge_base', {}).get('subjects', {})),
            'last_updated': data.get('project_context', {}).get('last_updated', 'Unknown')
        }
        
        return summary 