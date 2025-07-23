# 📚 Sahayak - AI Teaching Assistant

**Sahayak** (सहायक - meaning "Helper" in Hindi) is an AI-powered teaching assistant designed specifically for Indian classrooms. It supports multi-grade, multi-language, and multi-subject education across CBSE, ICSE, and State Board curricula.

## 🌟 Features

### 🎯 **Multi-Grade Support**
- **Primary (Class 1-5)**: Basic concepts with simple explanations
- **Middle (Class 6-8)**: Intermediate topics with detailed examples
- **Secondary (Class 9-10)**: Advanced concepts with comprehensive coverage
- **Higher Secondary (Class 11-12)**: Specialized subjects with in-depth analysis

### 🌐 **Multilingual Education**
- **English**: Native proficiency with clear, engaging content
- **Hindi**: Fluent support with सरल और आकर्षक content
- **Gujarati**: Fluent support with સરળ અને આકર્ષક content
- **Marathi**: Fluent support with सोपे आणि आकर्षक content
- **Bengali**: Good support with সহজ এবং আকর্ষণীয় content
- **Tamil**: Good support with எளிய மற்றும் கவர்ச்சிகரமான content
- **Telugu**: Good support with సరళమైన మరియు ఆకర్షణీయమైన content
- **Kannada**: Good support with ಸರಳ ಮತ್ತು ಆಕರ್ಷಕ content
- **Malayalam**: Good support with ലളിതവും ആകർഷകവുമായ content

### 📖 **Subject Expertise**
- **Mathematics**: Numbers, Algebra, Geometry, Trigonometry, Calculus
- **Science**: Physics, Chemistry, Biology, Environmental Science
- **Languages**: English, Hindi (Grammar, Literature, Writing)
- **Social Studies**: History, Geography, Civics, Economics
- **Computer Science**: Programming, Digital Literacy

### 🛠️ **Core Capabilities**

#### For Teachers:
- **📝 Lesson Planning**: Create structured, engaging lesson plans
- **📊 Worksheet Generation**: Generate practice sheets and assessments
- **🎨 Visual Aids**: Create diagrams, charts, and infographics
- **📋 Content Creation**: Generate explanations and examples
- **📈 Assessment Tools**: Create formative and summative evaluations

#### For Students:
- **❓ Homework Help**: Get step-by-step explanations
- **📚 Concept Understanding**: Ask questions in preferred language
- **🔢 Practice Problems**: Request additional exercises
- **🌍 Real-world Applications**: Connect concepts to daily life
- **🎯 Remedial Support**: Address learning gaps

#### For Parents:
- **📖 Progress Support**: Understand what children are learning
- **📚 Resource Recommendations**: Get additional learning materials
- **🏠 Homework Assistance**: Help with assignments
- **📊 Learning Insights**: Track educational progress

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd sahayak
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

Visit `http://localhost:5000` to start using Sahayak!

## 📋 Usage Examples

### For Teachers:

**Lesson Planning:**
```
"Create a lesson plan for teaching photosynthesis to Class 7 students"
"Design a 45-minute lesson on quadratic equations for Class 10"
"Generate a lesson plan for English grammar (Class 6)"
```

**Worksheet Creation:**
```
"Create a worksheet on fractions for Class 5 mathematics"
"Generate MCQ questions on the water cycle for Class 8"
"Design a practice sheet for Hindi grammar (Class 7)"
```

**Visual Aids:**
```
"Create a diagram showing the water cycle"
"Generate an infographic about photosynthesis"
"Design a chart for the periodic table"
```

### For Students:

**Homework Help:**
```
"मैं fractions को समझ नहीं पा रहा हूं" (I don't understand fractions)
"Explain photosynthesis in simple terms"
"How to solve quadratic equations step by step?"
"Help me write an essay on environmental conservation"
```

**Concept Understanding:**
```
"What is the difference between elements and compounds?"
"How does gravity work?"
"Explain the water cycle with examples"
"Help me understand algebraic expressions"
```

### For Parents:

**Support Queries:**
```
"How can I help my child with English grammar?"
"What are good resources for Class 8 science?"
"Help me understand what my child is learning in mathematics"
"How can I support my child's reading skills?"
```

## 🏗️ Architecture

### Core Components

```
Sahayak/
├── app/                    # Application core
│   ├── main.py            # Flask application
│   ├── assistant.py       # AI assistant logic
│   ├── config.py          # Configuration settings
│   ├── data_loader.py     # Data loading utilities
│   ├── data_updater.py    # Data update functionality
│   └── utils.py           # Utility functions
├── data/                   # Knowledge base
│   ├── personal_data.json # Sahayak's educational data
│   └── backups/           # Backup files
├── templates/              # HTML templates
├── static/                 # CSS and static files
├── prompts/                # AI prompts
└── requirements.txt        # Python dependencies
```

### Key Modules

- **`assistant.py`**: Core AI logic using Gemini API
- **`data_loader.py`**: Loads educational content and knowledge base
- **`data_updater.py`**: Updates educational data and content
- **`utils.py`**: Language detection, content formatting, validation

## 🔧 Configuration

### Environment Variables

```bash
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### Customizing Content

1. **Update Knowledge Base**: Modify `data/personal_data.json`
2. **Change AI Personality**: Edit `prompts/base_prompt.txt`
3. **Add New Subjects**: Update configuration in `app/config.py`

## 🌐 Deployment

### Local Development
```bash
python run.py
```

### Production (Render)
```bash
gunicorn wsgi:app
```

See `RENDER_DEPLOYMENT.md` for detailed deployment instructions.

## 📊 Data Structure

Sahayak uses a comprehensive JSON data structure to store:

```json
{
  "profile": {
    "name": "Sahayak",
    "type": "AI Teaching Assistant",
    "languages": ["English", "Hindi", "Gujarati", ...],
    "subjects": ["Mathematics", "Science", "English", ...],
    "grade_levels": ["Class 1-5", "Class 6-8", "Class 9-10", "Class 11-12"]
  },
  "content_generation": {
    "subjects": {
      "mathematics": {
        "topics": ["Numbers", "Algebra", "Geometry", ...],
        "difficulty_levels": ["Basic", "Intermediate", "Advanced"],
        "content_types": ["Explanations", "Examples", "Practice Problems"]
      }
    },
    "languages": {
      "english": {
        "proficiency": "Native",
        "content_style": "Clear, engaging, age-appropriate"
      }
    }
  },
  "worksheet_generation": {
    "types": {
      "practice_sheets": {
        "description": "Basic practice problems",
        "difficulty_levels": ["Easy", "Medium", "Hard"]
      }
    }
  },
  "lesson_planning": {
    "components": {
      "objectives": {
        "description": "Learning goals and outcomes",
        "types": ["Knowledge", "Understanding", "Application"]
      }
    }
  }
}
```

## 🔍 API Endpoints

- `GET /`: Main application interface
- `POST /chat`: Process educational queries
- `GET /health`: Health check endpoint
- `GET /result`: Display formatted results

## 🧪 Testing

Run the test suite:
```bash
python test_sahayak.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini AI**: For providing the AI capabilities
- **Indian Education System**: For inspiring the multi-grade, multi-language approach
- **Open Source Community**: For various libraries and tools used

## 📞 Support

- **Documentation**: Check `QUICK_START.md` for setup instructions
- **Deployment**: See `RENDER_DEPLOYMENT.md` for deployment guide
- **Issues**: Report bugs and feature requests via GitHub issues

## 🎯 Roadmap

- [ ] **Advanced Analytics**: Learning progress tracking
- [ ] **Voice Integration**: Speech-to-text and text-to-speech
- [ ] **Mobile App**: Native mobile application
- [ ] **Offline Mode**: Local AI model support
- [ ] **Collaborative Features**: Teacher-student interaction tools
- [ ] **Assessment Engine**: Automated grading and feedback
- [ ] **Content Library**: Pre-built lesson plans and worksheets
- [ ] **Parent Dashboard**: Progress monitoring and communication

---

**🎉 Sahayak - Empowering Indian Education with AI!**

*Making quality education accessible to every student, in every language, across every subject.*

