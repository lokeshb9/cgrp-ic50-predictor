"""
CGRP Receptor Antagonist IC50 Predictor
========================================

Professional ML application for predicting IC50 values of CGRP receptor antagonists.

Author: Dani Geiger
Version: 1.0.0
"""

import streamlit as st
import sys
from pathlib import Path
import logging

# Page config MUST be first!
st.set_page_config(
    page_title="CGRP IC50 Predictor",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from cgrp_predictor import Config, CGRPPredictor, DataProcessor
from cgrp_predictor.ui_components import UIComponents
from cgrp_predictor.content_manager import ContentManager
from cgrp_predictor.views import PredictorView, ResumeView, BiographyView

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CGRPApp:
    """Main application orchestrator."""
    
    def __init__(self):
        """Initialize app with dependencies."""
        self.config = Config()
        self.content = ContentManager()
        self.ui = UIComponents()
        self.data_processor = DataProcessor()
        
        # Load models (cached)
        self.predictor = self._load_predictor()
        
        # Load CSS
        self.ui.load_css()
        
        # Initialize views
        self.predictor_view = PredictorView(
            self.config, self.content, self.predictor, 
            self.data_processor, self.ui
        )
        self.resume_view = ResumeView(self.config, self.content, self.ui)
        self.biography_view = BiographyView(self.config, self.content, self.ui)
        
        logger.info("CGRP App initialized")
    
    @st.cache_resource
    def _load_predictor(_self) -> CGRPPredictor:
        """Load predictor model (cached)."""
        try:
            return CGRPPredictor(_self.config)
        except Exception as e:
            logger.error(f"Failed to load predictor: {e}")
            st.error(f"❌ Model loading failed: {e}")
            st.stop()
    
    def run(self):
        """Run the application."""
        # Create tabs
        tab1, tab2, tab3 = st.tabs([
            "🧬 CGRP Predictor",
            "📄 Resume",
            "👤 Biography"
        ])
        
        with tab1:
            self.predictor_view.render()
        
        with tab2:
            self.resume_view.render()
        
        with tab3:
            self.biography_view.render()
        
        # Footer
        self.ui.footer(version=self.config.app_version)


def main():
    """Main entry point."""
    try:
        app = CGRPApp()
        app.run()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"❌ Application failed: {e}")


if __name__ == "__main__":
    main()
