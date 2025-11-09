"""
Resume Tab View
===============

Handles rendering of professional resume/CV tab.
"""

import streamlit as st
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ResumeView:
    """Renders the resume/CV tab."""
    
    def __init__(self, config, content, ui):
        self.config = config
        self.content = content
        self.ui = ui
    
    def render(self):
        """Render complete resume tab."""
        self.ui.page_header("Resume", "Professional Background & Experience")
        
        # Display resume image
        resume_img = self.config.get_image_path('resume')
        if resume_img and resume_img.exists():
            st.image(str(resume_img), use_column_width=True)
        
        self._render_summary()
        self._render_education()
        self._render_experience()
        self._render_skills()
    
    def _render_summary(self):
        """Render professional summary section."""
        st.markdown("""
        ## 🎯 Professional Summary
        
        Passionate about **applying machine learning and AI to biomedical research**, with a focus on 
        **personalized medicine, biomarker analysis, and drug discovery**. Leveraging computational tools 
        to extract insights from NCBI research to improve diagnostics, treatment optimization, and healthcare accessibility.
        """)
    
    def _render_education(self):
        """Render education section."""
        st.markdown("## 🎓 Education")
        self.ui.timeline_item(
            "Bachelor of Science",
            "University of Oregon",
            "2017 - 2021",
            "Focus: Human Physiology, Biochemistry, Applications in Medicine"
        )
    
    def _render_experience(self):
        """Render experience section."""
        st.markdown("## 💼 Experience")
        
        self.ui.timeline_item(
            "Machine Learning & Bioinformatics Research",
            "Independent Research",
            "2021 - Present",
            """
            - Developed and applied **machine learning models** for biomarker discovery and drug screening
            - Conducted **biomarker analysis** using genomics, proteomics, and blood-based markers
            - Utilized **NCBI datasets** and AI-driven methods to analyze disease mechanisms
            - Integrated subjective and objective diagnostics using computational tools
            """
        )
        
        self.ui.timeline_item(
            "Inhalation Product Development (IPD)",
            "AstraZeneca",
            "2021",
            """
            - Worked with **biologic drug formulations** for inhalation delivery
            - Set up and operated **spray dryer** for mixing biologic drugs
            - Maintained **clean room conditions** and followed strict **GMP documentation**
            - Assisted in **document control** and regulatory compliance
            """
        )
    
    def _render_skills(self):
        """Render technical skills section."""
        st.markdown("## 🛠️ Technical Skills")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Programming & Data Science:**")
            self.ui.skill_badges([
                "Python", "Pandas", "NumPy", "Scikit-learn",
                "TensorFlow", "PyTorch", "Jupyter"
            ])
            
            st.markdown("**Bioinformatics & Computational Biology:**")
            self.ui.skill_badges([
                "RDKit", "PyMOL", "PaDEL", "ChEMBL",
                "RCSB PDB", "RNA-seq", "NCBI"
            ])
        
        with col2:
            st.markdown("**Machine Learning:**")
            self.ui.skill_badges([
                "Supervised Learning", "Unsupervised Learning",
                "Feature Engineering", "Model Selection",
                "Hyperparameter Tuning", "Cross-Validation"
            ])
            
            st.markdown("**Biomarker Analysis:**")
            self.ui.skill_badges([
                "Genomics", "Transcriptomics", "Proteomics",
                "Blood Biomarkers", "Clinical Data Analysis"
            ])

