"""
Utility functions for Sahayak - AI Teaching Assistant
Helper functions for educational content processing and analysis
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

def detect_language(text: str) -> str:
    """
    Detect the language of the input text
    Returns language code (english, hindi, gujarati, etc.)
    """
    # Simple language detection based on script
    if re.search(r'[\u0900-\u097F]', text):  # Devanagari script
        if re.search(r'[\u0A80-\u0AFF]', text):  # Gujarati
            return 'gujarati'
        else:
            return 'hindi'
    elif re.search(r'[\u0980-\u09FF]', text):  # Bengali
        return 'bengali'
    elif re.search(r'[\u0C80-\u0CFF]', text):  # Kannada
        return 'kannada'
    elif re.search(r'[\u0D00-\u0D7F]', text):  # Malayalam
        return 'malayalam'
    elif re.search(r'[\u0B80-\u0BFF]', text):  # Tamil
        return 'tamil'
    elif re.search(r'[\u0C00-\u0C7F]', text):  # Telugu
        return 'telugu'
    elif re.search(r'[\u0C80-\u0CFF]', text):  # Kannada
        return 'kannada'
    else:
        return 'english'

def detect_grade_level(text: str) -> str:
    """
    Detect the grade level from the input text
    Returns grade level (Class 1-5, Class 6-8, etc.)
    """
    text_lower = text.lower()
    
    # Primary level indicators
    if any(word in text_lower for word in ['class 1', 'class 2', 'class 3', 'class 4', 'class 5', 
                                          'grade 1', 'grade 2', 'grade 3', 'grade 4', 'grade 5',
                                          'primary', 'elementary', 'basic']):
        return 'Class 1-5'
    
    # Middle level indicators
    elif any(word in text_lower for word in ['class 6', 'class 7', 'class 8',
                                            'grade 6', 'grade 7', 'grade 8',
                                            'middle', 'junior']):
        return 'Class 6-8'
    
    # Secondary level indicators
    elif any(word in text_lower for word in ['class 9', 'class 10',
                                            'grade 9', 'grade 10',
                                            'secondary', 'high school']):
        return 'Class 9-10'
    
    # Higher secondary indicators
    elif any(word in text_lower for word in ['class 11', 'class 12',
                                            'grade 11', 'grade 12',
                                            'higher secondary', 'senior']):
        return 'Class 11-12'
    
    else:
        return 'Class 6-8'  # Default to middle level

def detect_subject(text: str) -> str:
    """
    Detect the subject from the input text
    Returns subject name (mathematics, science, etc.)
    """
    text_lower = text.lower()
    
    # Mathematics indicators
    if any(word in text_lower for word in ['math', 'mathematics', 'algebra', 'geometry', 
                                          'calculus', 'trigonometry', 'fractions', 'equations',
                                          'numbers', 'addition', 'subtraction', 'multiplication',
                                          'division', 'गणित', 'बीजगणित', 'ज्यामिति']):
        return 'mathematics'
    
    # Science indicators
    elif any(word in text_lower for word in ['science', 'physics', 'chemistry', 'biology',
                                            'experiment', 'lab', 'molecule', 'atom',
                                            'photosynthesis', 'gravity', 'energy',
                                            'विज्ञान', 'भौतिकी', 'रसायन', 'जीवविज्ञान']):
        return 'science'
    
    # English indicators
    elif any(word in text_lower for word in ['english', 'grammar', 'literature', 'essay',
                                            'writing', 'reading', 'comprehension',
                                            'अंग्रेजी', 'व्याकरण', 'साहित्य']):
        return 'english'
    
    # Hindi indicators
    elif any(word in text_lower for word in ['hindi', 'हिंदी', 'व्याकरण', 'साहित्य',
                                            'कविता', 'कहानी', 'निबंध']):
        return 'hindi'
    
    # Social Studies indicators
    elif any(word in text_lower for word in ['history', 'geography', 'civics', 'economics',
                                            'social studies', 'political', 'map',
                                            'इतिहास', 'भूगोल', 'नागरिक शास्त्र']):
        return 'social_studies'
    
    # Computer Science indicators
    elif any(word in text_lower for word in ['computer', 'programming', 'coding', 'software',
                                            'algorithm', 'data', 'digital', 'technology',
                                            'कंप्यूटर', 'प्रोग्रामिंग']):
        return 'computer_science'
    
    else:
        return 'general'

def format_lesson_plan(plan_data: Dict[str, Any]) -> str:
    """
    Format lesson plan data into a readable string
    """
    formatted = []
    
    if 'title' in plan_data:
        formatted.append(f"# {plan_data['title']}")
    
    if 'objectives' in plan_data:
        formatted.append("\n## Learning Objectives")
        for i, objective in enumerate(plan_data['objectives'], 1):
            formatted.append(f"{i}. {objective}")
    
    if 'materials' in plan_data:
        formatted.append("\n## Materials Required")
        for material in plan_data['materials']:
            formatted.append(f"- {material}")
    
    if 'activities' in plan_data:
        formatted.append("\n## Activities")
        for i, activity in enumerate(plan_data['activities'], 1):
            formatted.append(f"{i}. {activity}")
    
    if 'assessment' in plan_data:
        formatted.append("\n## Assessment")
        formatted.append(plan_data['assessment'])
    
    if 'duration' in plan_data:
        formatted.append(f"\n## Duration: {plan_data['duration']}")
    
    return "\n".join(formatted)

def format_worksheet(worksheet_data: Dict[str, Any]) -> str:
    """
    Format worksheet data into a readable string
    """
    formatted = []
    
    if 'title' in worksheet_data:
        formatted.append(f"# {worksheet_data['title']}")
    
    if 'instructions' in worksheet_data:
        formatted.append(f"\n## Instructions\n{worksheet_data['instructions']}")
    
    if 'questions' in worksheet_data:
        formatted.append("\n## Questions")
        for i, question in enumerate(worksheet_data['questions'], 1):
            formatted.append(f"{i}. {question}")
    
    if 'answer_key' in worksheet_data:
        formatted.append("\n## Answer Key")
        for i, answer in enumerate(worksheet_data['answer_key'], 1):
            formatted.append(f"{i}. {answer}")
    
    return "\n".join(formatted)

def get_content_insights(content_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate insights from content data
    """
    insights = {
        'total_subjects': len(content_data.get('subjects', {})),
        'total_languages': len(content_data.get('languages', {})),
        'content_types': [],
        'difficulty_levels': set(),
        'topics_count': 0
    }
    
    # Analyze subjects
    for subject, subject_data in content_data.get('subjects', {}).items():
        insights['content_types'].extend(subject_data.get('content_types', []))
        insights['difficulty_levels'].update(subject_data.get('difficulty_levels', []))
        insights['topics_count'] += len(subject_data.get('topics', []))
    
    insights['content_types'] = list(set(insights['content_types']))
    insights['difficulty_levels'] = list(insights['difficulty_levels'])
    
    return insights

def validate_educational_content(content: str, grade_level: str) -> Tuple[bool, List[str]]:
    """
    Validate educational content for appropriateness
    Returns (is_valid, list_of_issues)
    """
    issues = []
    
    # Check content length
    if len(content) < 50:
        issues.append("Content is too short")
    elif len(content) > 5000:
        issues.append("Content is too long")
    
    # Check for inappropriate content
    inappropriate_words = ['inappropriate', 'offensive', 'harmful']
    for word in inappropriate_words:
        if word in content.lower():
            issues.append(f"Content contains inappropriate language: {word}")
    
    # Grade-specific validation
    if grade_level == 'Class 1-5':
        # Check for complex vocabulary
        complex_words = ['sophisticated', 'complicated', 'advanced', 'complex']
        for word in complex_words:
            if word in content.lower():
                issues.append(f"Content may be too complex for primary level: {word}")
    
    return len(issues) == 0, issues

def generate_content_summary(content: str, max_length: int = 200) -> str:
    """
    Generate a summary of educational content
    """
    if len(content) <= max_length:
        return content
    
    # Simple summary by taking first few sentences
    sentences = re.split(r'[.!?]+', content)
    summary = ""
    
    for sentence in sentences:
        if len(summary + sentence) < max_length:
            summary += sentence + ". "
        else:
            break
    
    return summary.strip()

def extract_keywords(text: str) -> List[str]:
    """
    Extract key educational terms from text
    """
    # Common educational keywords
    keywords = [
        'learn', 'teach', 'study', 'practice', 'understand', 'explain',
        'solve', 'calculate', 'analyze', 'evaluate', 'create', 'design',
        'experiment', 'observe', 'measure', 'compare', 'contrast',
        'summarize', 'describe', 'identify', 'define', 'classify'
    ]
    
    found_keywords = []
    text_lower = text.lower()
    
    for keyword in keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def format_timestamp(timestamp: Optional[str] = None) -> str:
    """
    Format timestamp for display
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return timestamp

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def create_backup_filename(prefix: str = "sahayak") -> str:
    """
    Create a backup filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_backup_{timestamp}.json"
