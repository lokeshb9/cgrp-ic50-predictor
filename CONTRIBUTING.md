# Contributing to CGRP Predictor

## 🚀 Quick Start for Developers

### Prerequisites
- Python 3.9+
- Java Runtime Environment (for PaDEL)

### Installation
```bash
# Clone and navigate
cd cgrp-ic50-predictor

# Create environment
pyenv virtualenv 3.12.11 cgrp-project
pyenv local cgrp-project

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install as editable package
pip install -e .
```

### Run the App
```bash
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
streamlit run app.py
```

---

## 📁 Project Structure

```
├── app.py                          # Main application (111 lines)
├── src/cgrp_predictor/             # Source code
│   ├── config.py                   # Configuration management
│   ├── data_processor.py           # Data validation
│   ├── predictor.py                # ML predictions
│   ├── fingerprint_generator.py    # PaDEL integration
│   ├── content_manager.py          # Content management
│   ├── ui_components.py            # UI components
│   └── views/                      # Page views (MVC pattern)
│       ├── predictor_view.py       # Prediction tab
│       ├── resume_view.py          # Resume tab
│       └── biography_view.py       # Biography tab
├── tests/                          # Test suite
├── config/                         # Configuration files
│   ├── config.yaml                 # App settings
│   └── content.yaml                # User-facing text
├── assets/                         # Static assets
│   ├── css/style.css               # Custom styling
│   └── images/                     # Images
├── models/                         # ML models
└── data/                           # Example data
```

---

## 🛠️ Development

### Running Tests
```bash
pytest                    # All tests
pytest --cov             # With coverage
pytest -v                # Verbose
```

### Code Quality
```bash
black src/               # Format code
flake8 src/              # Lint
mypy src/                # Type check
```

### Making Changes

1. **Edit content** → Modify `config/content.yaml` (restart app)
2. **Edit styling** → Modify `assets/css/style.css` (hard refresh browser)
3. **Edit code** → Modify `src/*.py` (auto-reloads with watchdog)
4. **Edit config** → Modify `config/config.yaml` (restart app)

---

## 📝 Editing Content

All user-facing text is in `config/content.yaml`:

```yaml
biography_tab:
  header:
    name: "Your Name"          # Edit this!
    title: "Your Title"        # Edit this!
```

No Python knowledge needed!

---

## 🎨 Architecture

- **MVC Pattern**: Views separated from models
- **Singleton**: Config and ContentManager
- **Dependency Injection**: Clean testing
- **Separation of Concerns**: Each module has one job

---

## 🧪 Testing

- Unit tests in `tests/unit/`
- Coverage goal: >80%
- Run before committing: `pytest`

---

## 📚 Documentation

### For Users
- **README.md** - Installation, usage, overview

### For Developers
- **CONTRIBUTING.md** (this file) - Development guide
- **ARCHITECTURE.md** - Technical details
- Inline docstrings - API documentation

---

## 🔄 Development Workflow

1. Create feature branch
2. Make changes
3. Write/update tests
4. Run `pytest`
5. Format code: `black src/`
6. Commit with clear message

---

## 📞 Questions?

- Check inline docstrings in source code
- Review `ARCHITECTURE.md` for technical details
- See `config/content.yaml` for text content

