"""
Visual Aids Generator for Sahayak AI Teaching Assistant
Generates educational images, diagrams, charts, and visual content for Indian classrooms
"""

import json
import base64
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import io
import os

class VisualAidsGenerator:
    def __init__(self, api_key: str):
        """Initialize the visual aids generator with Google AI"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision')
        self.text_model = genai.GenerativeModel('gemini-pro')
        
    def generate_educational_image(self, subject: str, topic: str, grade: str, 
                                 language: str = "English", style: str = "simple") -> Dict:
        """
        Generate educational images using AI prompts optimized for Indian classrooms
        
        Args:
            subject: Subject (Math, Science, English, Hindi, etc.)
            topic: Specific topic to visualize
            grade: Grade level (1-12)
            language: Language for labels (English, Hindi, Marathi, etc.)
            style: Visual style (simple, colorful, cartoon, realistic)
            
        Returns:
            Dict with image data and metadata
        """
        try:
            # Create detailed prompt for Indian classroom context
            prompt = self._create_image_prompt(subject, topic, grade, language, style)
            
            # For now, we'll create a placeholder image since we can't generate images directly
            # In production, this would integrate with Google's image generation API
            image_data = self._create_placeholder_image(topic, subject, grade)
            
            return {
                "success": True,
                "image_data": image_data,
                "metadata": {
                    "subject": subject,
                    "topic": topic,
                    "grade": grade,
                    "language": language,
                    "style": style,
                    "type": "educational_image"
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
    
    def create_diagram(self, diagram_type: str, data: Dict, 
                      language: str = "English") -> Dict:
        """
        Create educational diagrams (flowcharts, mind maps, etc.)
        
        Args:
            diagram_type: Type of diagram (flowchart, mindmap, venn, timeline)
            data: Data to visualize
            language: Language for labels
            
        Returns:
            Dict with diagram data
        """
        try:
            # Create diagram using PIL
            diagram_data = self._generate_diagram(diagram_type, data, language)
            
            return {
                "success": True,
                "diagram_data": diagram_data,
                "metadata": {
                    "type": diagram_type,
                    "language": language,
                    "data_points": len(data)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "type": diagram_type,
                    "language": language
                }
            }
    
    def generate_chart(self, chart_type: str, data: Dict, 
                      title: str, language: str = "English") -> Dict:
        """
        Generate educational charts and graphs
        
        Args:
            chart_type: Type of chart (bar, pie, line, histogram)
            data: Data to visualize
            title: Chart title
            language: Language for labels
            
        Returns:
            Dict with chart data
        """
        try:
            # Create chart using PIL
            chart_data = self._generate_chart_image(chart_type, data, title, language)
            
            return {
                "success": True,
                "chart_data": chart_data,
                "metadata": {
                    "type": chart_type,
                    "title": title,
                    "language": language,
                    "data_points": len(data)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "type": chart_type,
                    "title": title,
                    "language": language
                }
            }
    
    def create_flashcards(self, topic: str, cards_data: List[Dict], 
                         language: str = "English") -> Dict:
        """
        Generate educational flashcards
        
        Args:
            topic: Topic for flashcards
            cards_data: List of question-answer pairs
            language: Language for content
            
        Returns:
            Dict with flashcards data
        """
        try:
            flashcards = []
            for i, card in enumerate(cards_data):
                flashcard = self._create_single_flashcard(
                    card.get("question", ""),
                    card.get("answer", ""),
                    i + 1,
                    language
                )
                flashcards.append(flashcard)
            
            return {
                "success": True,
                "flashcards": flashcards,
                "metadata": {
                    "topic": topic,
                    "language": language,
                    "count": len(cards_data)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {
                    "topic": topic,
                    "language": language
                }
            }
    
    def _create_image_prompt(self, subject: str, topic: str, grade: str, 
                           language: str, style: str) -> str:
        """Create detailed prompt for image generation"""
        
        language_context = {
            "Hindi": "Use Hindi labels and text where appropriate",
            "Marathi": "Use Marathi labels and text where appropriate", 
            "Tamil": "Use Tamil labels and text where appropriate",
            "Telugu": "Use Telugu labels and text where appropriate",
            "Bengali": "Use Bengali labels and text where appropriate",
            "English": "Use clear English labels"
        }
        
        grade_context = {
            "1-3": "Simple, colorful, large elements, minimal text",
            "4-6": "Clear, engaging, moderate complexity",
            "7-9": "Detailed, informative, professional style",
            "10-12": "Advanced, comprehensive, academic style"
        }
        
        style_context = {
            "simple": "Clean, minimal design with clear lines",
            "colorful": "Bright, engaging colors suitable for children",
            "cartoon": "Friendly, animated style with characters",
            "realistic": "Photorealistic or detailed illustrations"
        }
        
        prompt = f"""
        Create an educational image for {subject} topic: {topic}
        
        Context:
        - Grade level: {grade} ({grade_context.get(grade, 'Appropriate complexity')})
        - Language: {language} ({language_context.get(language, 'Clear labels')})
        - Style: {style} ({style_context.get(style, 'Professional')})
        
        Requirements:
        - Suitable for Indian classroom context
        - Culturally appropriate and relevant
        - Clear, educational value
        - Accessible for students with different learning styles
        - Include visual elements that support learning objectives
        
        Focus on creating an image that:
        1. Clearly illustrates the concept
        2. Uses appropriate colors and visual hierarchy
        3. Includes necessary labels and annotations
        4. Is engaging and memorable for students
        5. Supports the learning objectives for this grade level
        """
        
        return prompt
    
    def _create_placeholder_image(self, topic: str, subject: str, grade: str) -> str:
        """Create a placeholder image using PIL"""
        try:
            # Create a simple placeholder image
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # Try to use a default font, fallback to basic if not available
            try:
                font = ImageFont.truetype("arial.ttf", 24)
                small_font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Draw title
            title = f"{subject}: {topic}"
            draw.text((width//2 - 100, 50), title, fill='black', font=font)
            
            # Draw placeholder content
            draw.rectangle([100, 150, 700, 450], outline='blue', width=3)
            draw.text((width//2 - 80, 200), "Educational Image", fill='blue', font=font)
            draw.text((width//2 - 120, 250), f"Topic: {topic}", fill='black', font=small_font)
            draw.text((width//2 - 100, 280), f"Grade: {grade}", fill='black', font=small_font)
            draw.text((width//2 - 150, 320), "Visual content will be generated here", fill='gray', font=small_font)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_data = base64.b64encode(buffer.getvalue()).decode()
            
            return image_data
            
        except Exception as e:
            # Return a simple text representation if image creation fails
            return f"Image placeholder for {topic} ({subject}, Grade {grade})"
    
    def _generate_diagram(self, diagram_type: str, data: Dict, language: str) -> str:
        """Generate diagram image"""
        try:
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Draw diagram title
            title = f"{diagram_type.title()} Diagram"
            draw.text((width//2 - 80, 30), title, fill='black', font=font)
            
            # Simple diagram representation
            if diagram_type == "flowchart":
                self._draw_flowchart(draw, data, width, height, font)
            elif diagram_type == "mindmap":
                self._draw_mindmap(draw, data, width, height, font)
            elif diagram_type == "venn":
                self._draw_venn_diagram(draw, data, width, height, font)
            else:
                # Generic diagram
                draw.rectangle([100, 100, 700, 500], outline='black', width=2)
                draw.text((width//2 - 100, 250), f"{diagram_type} diagram", fill='black', font=font)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode()
            
        except Exception as e:
            return f"Diagram placeholder for {diagram_type}"
    
    def _draw_flowchart(self, draw, data, width, height, font):
        """Draw a simple flowchart"""
        # Draw boxes
        boxes = [
            (width//2 - 100, 100, width//2 + 100, 150),
            (width//2 - 100, 200, width//2 + 100, 250),
            (width//2 - 100, 300, width//2 + 100, 350),
            (width//2 - 100, 400, width//2 + 100, 450)
        ]
        
        for i, box in enumerate(boxes):
            draw.rectangle(box, outline='blue', width=2)
            draw.text((box[0] + 10, box[1] + 20), f"Step {i+1}", fill='black', font=font)
            
            # Draw arrows
            if i < len(boxes) - 1:
                draw.line([(box[2], box[1] + 25), (box[2] + 50, box[1] + 25), 
                          (box[2] + 50, boxes[i+1][1] + 25), (boxes[i+1][0], boxes[i+1][1] + 25)], 
                         fill='black', width=2)
    
    def _draw_mindmap(self, draw, data, width, height, font):
        """Draw a simple mindmap"""
        center_x, center_y = width//2, height//2
        
        # Draw center
        draw.ellipse([center_x - 50, center_y - 30, center_x + 50, center_y + 30], 
                    outline='red', width=3)
        draw.text((center_x - 30, center_y - 10), "Topic", fill='black', font=font)
        
        # Draw branches
        branches = [
            (center_x + 80, center_y - 60, "Branch 1"),
            (center_x + 80, center_y, "Branch 2"),
            (center_x + 80, center_y + 60, "Branch 3"),
            (center_x - 80, center_y - 60, "Branch 4"),
            (center_x - 80, center_y, "Branch 5"),
            (center_x - 80, center_y + 60, "Branch 6")
        ]
        
        for x, y, text in branches:
            draw.ellipse([x - 30, y - 20, x + 30, y + 20], outline='blue', width=2)
            draw.text((x - 20, y - 5), text, fill='black', font=font)
            draw.line([(center_x + 50, center_y), (x - 30, y)], fill='black', width=2)
    
    def _draw_venn_diagram(self, draw, data, width, height, font):
        """Draw a simple Venn diagram"""
        center_x, center_y = width//2, height//2
        
        # Draw two overlapping circles
        draw.ellipse([center_x - 100, center_y - 80, center_x, center_y + 80], 
                    outline='blue', width=3)
        draw.ellipse([center_x, center_y - 80, center_x + 100, center_y + 80], 
                    outline='red', width=3)
        
        # Add labels
        draw.text((center_x - 80, center_y - 100), "Set A", fill='blue', font=font)
        draw.text((center_x + 60, center_y - 100), "Set B", fill='red', font=font)
        draw.text((center_x - 20, center_y), "A ∩ B", fill='purple', font=font)
    
    def _generate_chart_image(self, chart_type: str, data: Dict, title: str, language: str) -> str:
        """Generate chart image"""
        try:
            width, height = 800, 600
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Draw title
            draw.text((width//2 - 100, 30), title, fill='black', font=font)
            
            # Simple chart representation
            if chart_type == "bar":
                self._draw_bar_chart(draw, data, width, height, font)
            elif chart_type == "pie":
                self._draw_pie_chart(draw, data, width, height, font)
            elif chart_type == "line":
                self._draw_line_chart(draw, data, width, height, font)
            else:
                # Generic chart
                draw.rectangle([100, 100, 700, 500], outline='black', width=2)
                draw.text((width//2 - 80, 250), f"{chart_type} chart", fill='black', font=font)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode()
            
        except Exception as e:
            return f"Chart placeholder for {chart_type}"
    
    def _draw_bar_chart(self, draw, data, width, height, font):
        """Draw a simple bar chart"""
        chart_area = [100, 100, 700, 500]
        draw.rectangle(chart_area, outline='black', width=2)
        
        # Draw bars
        bar_width = 60
        spacing = 40
        start_x = chart_area[0] + 50
        
        for i, (label, value) in enumerate(data.items()):
            x = start_x + i * (bar_width + spacing)
            bar_height = min(value * 10, 300)  # Scale the value
            y = chart_area[3] - bar_height - 20
            
            draw.rectangle([x, y, x + bar_width, chart_area[3] - 20], 
                          fill='blue', outline='black')
            draw.text((x, chart_area[3] - 10), str(label), fill='black', font=font)
    
    def _draw_pie_chart(self, draw, data, width, height, font):
        """Draw a simple pie chart"""
        center_x, center_y = width//2, height//2
        radius = 150
        
        # Draw pie chart outline
        draw.ellipse([center_x - radius, center_y - radius, 
                     center_x + radius, center_y + radius], 
                    outline='black', width=2)
        
        # Add legend
        y_offset = 50
        for i, (label, value) in enumerate(data.items()):
            color = ['red', 'blue', 'green', 'yellow', 'purple'][i % 5]
            draw.rectangle([center_x + radius + 20, center_y - radius + y_offset,
                           center_x + radius + 40, center_y - radius + y_offset + 20], 
                          fill=color)
            draw.text((center_x + radius + 50, center_y - radius + y_offset), 
                     f"{label}: {value}", fill='black', font=font)
            y_offset += 30
    
    def _draw_line_chart(self, draw, data, width, height, font):
        """Draw a simple line chart"""
        chart_area = [100, 100, 700, 500]
        draw.rectangle(chart_area, outline='black', width=2)
        
        # Draw line
        points = []
        for i, (label, value) in enumerate(data.items()):
            x = chart_area[0] + 50 + i * 100
            y = chart_area[3] - 20 - min(value * 10, 300)
            points.append((x, y))
        
        if len(points) > 1:
            draw.line(points, fill='red', width=3)
        
        # Draw points
        for x, y in points:
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill='red')
    
    def _create_single_flashcard(self, question: str, answer: str, 
                                card_number: int, language: str) -> Dict:
        """Create a single flashcard"""
        try:
            width, height = 400, 300
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            try:
                font = ImageFont.truetype("arial.ttf", 14)
                title_font = ImageFont.truetype("arial.ttf", 18)
            except:
                font = ImageFont.load_default()
                title_font = ImageFont.load_default()
            
            # Draw card border
            draw.rectangle([10, 10, width-10, height-10], outline='blue', width=3)
            
            # Draw card number
            draw.text((20, 20), f"Card {card_number}", fill='blue', font=title_font)
            
            # Draw question
            draw.text((20, 60), "Question:", fill='black', font=title_font)
            draw.text((20, 90), question[:50] + "..." if len(question) > 50 else question, 
                     fill='black', font=font)
            
            # Draw answer
            draw.text((20, 150), "Answer:", fill='black', font=title_font)
            draw.text((20, 180), answer[:50] + "..." if len(answer) > 50 else answer, 
                     fill='black', font=font)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_data = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                "card_number": card_number,
                "question": question,
                "answer": answer,
                "image_data": image_data
            }
            
        except Exception as e:
            return {
                "card_number": card_number,
                "question": question,
                "answer": answer,
                "image_data": f"Flashcard {card_number} placeholder"
            } 