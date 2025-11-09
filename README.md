# CGRP Receptor Antagonist IC50 Predictor

A professional, production-grade machine learning application for predicting IC50 values of CGRP (Calcitonin Gene-Related Peptide) receptor antagonists - potential treatments for migraines.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)

## 🎯 Project Overview

This project uses Random Forest regression on molecular fingerprints to predict the inhibitory concentration (IC50) of small molecules against the CGRP receptor. The model was trained on 538 bioactivity measurements from the ChEMBL database.

### Personal Motivation

This project was inspired by complications my mother experienced with CGRP-targeting monoclonal antibody treatments for her chronic migraines. The goal is to identify safer small-molecule alternatives that could provide effective treatment without adverse effects.

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| R² Score | 0.82 |
| RMSE | 0.445 (standardized) |
| Training Samples | 430 compounds |
| Test Samples | 108 compounds |
| Features | 133 (post variance-threshold) |
| Algorithm | Random Forest (175 trees) |
| Models Tested | 504 combinations |
| Hyperparameter Combos | 8,784 total |

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** (tested with Python 3.12)
- **Java Runtime Environment** (required for PaDEL)

**Install Java:**
```bash
# macOS
brew install openjdk

# Windows/Linux: https://www.java.com
```

### Installation

```bash
# Clone repository
git clone https://github.com/danigeiger/CGRP_gepant_ML_project.git
cd CGRP_gepant_ML_project

# Create virtual environment
pyenv virtualenv 3.12.11 cgrp-project
pyenv local cgrp-project

# Install dependencies
pip install -r requirements.txt

# Install as package (optional)
pip install -e .
```

### Run the Application

```bash
# Set Java path (macOS)
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"

# Run the app
streamlit run app.py
```

Open browser to: `http://localhost:8501`

## 📖 Usage

### Web Interface

1. **Upload file** - CSV or TXT with ChEMBL IDs and SMILES (auto-detected)
2. **Wait ~3 seconds** - Fingerprints generated automatically
3. **View results** - Color-coded predictions with distribution chart
4. **Download CSV** - Export complete results

### File Format

```csv
CHEMBL200715,Oc1cc(O)c2c(c1)O[C@@H](c1ccc(O)c(O)c1)[C@H](O)C2
CHEMBL311498,Oc1cc(O)c2c(c1)O[C@H](c1ccc(O)c(O)c1)[C@@H](O)C2
```

**Requirements:** 2 columns (ChEMBL_ID, SMILES) • No headers • CSV or TXT format

## 📁 Project Structure

```
├── app.py                          # Main application (refactored, 111 lines)
├── src/cgrp_predictor/             # Source code package
│   ├── config.py                   # Configuration management
│   ├── data_processor.py           # Data validation & processing
│   ├── predictor.py                # ML prediction pipeline
│   ├── fingerprint_generator.py    # PaDEL integration
│   ├── content_manager.py          # Content management (separation of concerns)
│   ├── ui_components.py            # Reusable UI components
│   └── views/                      # MVC pattern
│       ├── predictor_view.py       # Prediction interface
│       ├── resume_view.py          # Resume tab
│       └── biography_view.py       # Biography tab
├── tests/unit/                     # Unit tests (pytest)
├── config/                         # Configuration files
│   ├── config.yaml                 # App settings
│   └── content.yaml                # User-facing text (easy editing)
├── assets/                         # Static files
│   ├── css/style.css               # Custom styling (400+ lines)
│   └── images/                     # Images
├── models/                         # ML models
│   ├── rf_reg.joblib              # Random Forest model
│   ├── target_scaler.joblib       # StandardScaler
│   └── variance_selector.joblib   # Feature selector
├── data/                           # Example data
└── notebooks/                      # Analysis notebooks
    ├── CGRP_Analysis.ipynb
    ├── lazy_predict.ipynb
    └── CGRP_model_hypertuning.ipynb
```

## 🔬 Methodology

### 1. Data Collection
- **Source**: ChEMBL database (CHEMBL3798)
- **Compounds**: 538 unique molecules
- **Metric**: IC50 (inhibitory concentration)

### 2. Feature Engineering
- **Input**: Canonical SMILES strings
- **Tool**: PaDEL-Descriptor
- **Output**: 881 binary molecular fingerprints
- **Feature Selection**: Variance threshold → 133 features

### 3. Model Development
- **Tested**: 42 algorithms × 12 configurations = 504 models
- **Top 3**: Bagging, Random Forest, Gradient Boosting
- **Hyperparameter Tuning**: 8,784 combinations via GridSearchCV
- **Winner**: Random Forest (best generalization, 82% R²)

### 4. Production Deployment
- Modular architecture (SOLID principles)
- Comprehensive testing (pytest)
- Configuration management (YAML)
- Professional UI/UX
- Complete documentation

## 🛠️ Tech Stack

- **ML**: scikit-learn, NumPy, pandas
- **Cheminformatics**: PaDEL-Descriptor
- **Web**: Streamlit, Altair (charts)
- **Config**: PyYAML
- **Testing**: pytest
- **Package**: setuptools

## ✨ Features

- ✅ **Professional UI** with custom CSS and animations
- ✅ **Auto-detect file format** (CSV/TXT)
- ✅ **Real-time progress** indicators
- ✅ **Interactive charts** with Altair
- ✅ **Color-coded results** (🟢🟡🔴)
- ✅ **Comprehensive testing** (unit tests)
- ✅ **Modular architecture** (MVC pattern)
- ✅ **Configuration management** (no hardcoded values)
- ✅ **Content management** (easy text editing)
- ✅ **Production logging**
- ✅ **Error handling** with helpful messages

## ⚠️ Limitations

- Computational estimates only (not experimental measurements)
- Best for small molecules (<2,000 Daltons)
- Most accurate for gepant-like structures
- Requires Java Runtime Environment

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=src/cgrp_predictor

# Verbose output
pytest -v
```

**Test Coverage:** >80% for core modules

## 🎨 Customization

### Edit Content (No Coding Required!)
Edit `config/content.yaml` to change any text:
```yaml
biography_tab:
  header:
    name: "Your Name"
    title: "Your Title"
```

### Edit Configuration
Edit `config/config.yaml` for settings:
```yaml
predictions:
  ic50_thresholds:
    active_max: 1000
```

### Edit Styling
Edit `assets/css/style.css` for visual changes

## 📚 Documentation

- **README.md** (this file) - Overview and quick start
- **CONTRIBUTING.md** - Development guide and architecture
- Inline docstrings - Complete API documentation

## 📈 Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Project architecture
- Testing guidelines
- Code quality standards

## 👩‍💻 Author

**Dani Geiger**
- B.S. Human Physiology, Biochemistry - University of Oregon (2017-2021)
- Experience: AstraZeneca - Inhalation Product Development
- Interests: AI-driven drug discovery, precision medicine

## 🙏 Acknowledgments

- **Chanin Nantasenamat** - ChEMBL data curation guidance
- **Shankar Pandala** - LazyPredict library
- **My mother** - Inspiration for this research

## 📝 License

MIT License - Free for research and educational use

## 📞 Contact

- **GitHub**: [github.com/danigeiger](https://github.com/danigeiger)
- **Project**: [CGRP Predictor](https://github.com/danigeiger/CGRP_gepant_ML_project)

---

*"For those who suffer from chronic migraines - may better treatments be found."*
