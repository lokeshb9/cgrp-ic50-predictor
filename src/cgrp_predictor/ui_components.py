"""
Streamlit UI Components
========================

Reusable, professional UI components for the CGRP Predictor web interface.
Provides consistent styling and structure across all pages.

Author: Dani Geiger
"""

import streamlit as st
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class UIComponents:
    """
    Professional UI component library for Streamlit applications.
    
    Provides reusable, consistently-styled components including:
    - Info boxes (success, warning, error, info)
    - Metric cards
    - Timeline displays
    - Skill badges
    - Research interest tags
    
    Example:
        >>> ui = UIComponents()
        >>> ui.success_box("Operation completed successfully!")
        >>> ui.metric_card("Model Accuracy", "82.5%", "R² Score")
    """
    
    @staticmethod
    def load_css(css_file: str = "assets/css/style.css") -> None:
        """
        Load custom CSS stylesheet.
        
        Args:
            css_file: Path to CSS file relative to project root
        """
        try:
            css_path = Path(css_file)
            if css_path.exists():
                with open(css_path) as f:
                    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
                logger.info(f"Loaded CSS from {css_file}")
            else:
                logger.warning(f"CSS file not found: {css_file}")
        except Exception as e:
            logger.error(f"Failed to load CSS: {e}")
    
    @staticmethod
    def info_box(message: str) -> None:
        """Display informational message box."""
        st.markdown(
            f'<div class="info-box">ℹ️ {message}</div>',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def success_box(message: str) -> None:
        """Display success message box."""
        st.markdown(
            f'<div class="success-box">✅ {message}</div>',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def warning_box(message: str) -> None:
        """Display warning message box."""
        st.markdown(
            f'<div class="warning-box">⚠️ {message}</div>',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def error_box(message: str) -> None:
        """Display error message box."""
        st.markdown(
            f'<div class="error-box">❌ {message}</div>',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def metric_card(title: str, value: str, subtitle: str = "") -> None:
        """
        Display metric in a styled card.
        
        Args:
            title: Metric title
            value: Metric value
            subtitle: Optional subtitle/description
        """
        subtitle_html = f'<p style="color: #6c757d; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ""
        st.markdown(
            f'''
            <div class="metric-card">
                <h3 style="margin-top: 0;">{title}</h3>
                <h2 style="color: #1f77b4; margin: 0.5rem 0;">{value}</h2>
                {subtitle_html}
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def prediction_card(ic50_value: float, classification: str) -> None:
        """
        Display IC50 prediction in a styled card.
        
        Args:
            ic50_value: Predicted IC50 in nM
            classification: Activity classification
        """
        emoji_map = {
            'active': '🟢',
            'intermediate': '🟡',
            'inactive': '🔴'
        }
        emoji = emoji_map.get(classification.lower(), '⚪')
        
        st.markdown(
            f'''
            <div class="prediction-card fade-in">
                <h2 style="margin-top: 0; color: white;">Predicted IC50</h2>
                <h1 style="color: white; margin: 1rem 0; border: none;">{ic50_value:.2f} nM</h1>
                <p style="font-size: 1.2rem; margin: 0;">{emoji} {classification}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def timeline_item(title: str, organization: str, date: str, description: str) -> None:
        """
        Display timeline item for resume/experience.
        
        Args:
            title: Position/role title
            organization: Company/institution name
            date: Date range
            description: Description of role/achievements
        """
        st.markdown(
            f'''
            <div class="timeline-item">
                <h3 style="margin-top: 0; color: #1f77b4;">{title}</h3>
                <p style="color: #6c757d; margin: 0.3rem 0;"><strong>{organization}</strong> | {date}</p>
                <p style="margin-top: 1rem;">{description}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def skill_badges(skills: List[str]) -> None:
        """
        Display skills as styled badges.
        
        Args:
            skills: List of skill names
        """
        badges_html = "".join([
            f'<span class="skill-badge">{skill}</span>'
            for skill in skills
        ])
        st.markdown(badges_html, unsafe_allow_html=True)
    
    @staticmethod
    def research_tags(topics: List[str]) -> None:
        """
        Display research interests as styled tags.
        
        Args:
            topics: List of research topics
        """
        tags_html = "".join([
            f'<span class="research-tag">{topic}</span>'
            for topic in topics
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    @staticmethod
    def bio_header(name: str, title: str, tagline: str) -> None:
        """
        Display biography header section.
        
        Args:
            name: Person's name
            title: Professional title
            tagline: Personal tagline/motto
        """
        st.markdown(
            f'''
            <div class="bio-header">
                <h1 style="color: white; border: none; margin: 0;">{name}</h1>
                <h3 style="color: rgba(255,255,255,0.9); margin: 0.5rem 0;">{title}</h3>
                <p style="font-size: 1.1rem; color: rgba(255,255,255,0.8); margin-top: 1rem;">{tagline}</p>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def bio_card(title: str, content: str, icon: str = "📝") -> None:
        """
        Display biography content card.
        
        Args:
            title: Card title
            content: Card content (supports HTML)
            icon: Emoji icon for the card
        """
        st.markdown(
            f'''
            <div class="bio-card">
                <h2 style="color: #1f77b4; margin-top: 0;">{icon} {title}</h2>
                <div style="line-height: 1.8; color: #2c3e50;">{content}</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def classification_badge(classification: str) -> str:
        """
        Get HTML for classification badge.
        
        Args:
            classification: Activity classification
            
        Returns:
            str: HTML for styled badge
        """
        class_map = {
            'active': 'active-badge',
            'intermediate': 'intermediate-badge',
            'inactive': 'inactive-badge'
        }
        badge_class = class_map.get(classification.lower(), 'inactive-badge')
        return f'<span class="{badge_class}">{classification}</span>'
    
    @staticmethod
    def page_header(title: str, subtitle: str = "") -> None:
        """
        Display page header with title and optional subtitle.
        
        Args:
            title: Page title
            subtitle: Optional subtitle
        """
        st.markdown(f'<h1>{title}</h1>', unsafe_allow_html=True)
        if subtitle:
            st.markdown(
                f'<p style="font-size: 1.2rem; color: #6c757d; margin-top: -1rem;">{subtitle}</p>',
                unsafe_allow_html=True
            )
    
    @staticmethod
    def footer(version: str = "1.0.0") -> None:
        """
        Display application footer.
        
        Args:
            version: Application version
        """
        st.markdown(
            f'''
            <div class="footer">
                <p><strong>CGRP Predictor</strong> v{version} | Built with ❤️ for better migraine treatments</p>
                <p style="font-size: 0.8rem; margin-top: 0.5rem;">
                    © 2025 Dani Geiger | MIT License
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def create_columns_with_images(
        images: List[str],
        captions: List[str] = None,
        width: int = None
    ) -> None:
        """
        Create columns with images displayed side-by-side.
        
        Args:
            images: List of image paths
            captions: Optional list of captions
            width: Optional width for images
        """
        cols = st.columns(len(images))
        for i, (col, img_path) in enumerate(zip(cols, images)):
            with col:
                if Path(img_path).exists():
                    caption = captions[i] if captions and i < len(captions) else None
                    st.image(img_path, use_column_width=True, caption=caption)
                else:
                    logger.warning(f"Image not found: {img_path}")


class StreamlitHelpers:
    """
    Helper functions for common Streamlit operations.
    """
    
    @staticmethod
    def set_page_config(
        title: str,
        icon: str = "🧬",
        layout: str = "wide"
    ) -> None:
        """
        Configure Streamlit page settings.
        
        Args:
            title: Page title
            icon: Page icon emoji
            layout: Layout style ('centered' or 'wide')
        """
        st.set_page_config(
            page_title=title,
            page_icon=icon,
            layout=layout,
            initial_sidebar_state="expanded"
        )
    
    @staticmethod
    def hide_streamlit_style() -> None:
        """Hide default Streamlit UI elements for cleaner appearance."""
        hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
        st.markdown(hide_st_style, unsafe_allow_html=True)

