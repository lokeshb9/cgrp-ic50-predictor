"""
Biography Tab View
==================

Handles rendering of personal biography tab with beautiful styling.
"""

import streamlit as st
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class BiographyView:
    """Renders the biography/personal story tab."""
    
    def __init__(self, config, content, ui):
        self.config = config
        self.content = content
        self.ui = ui
        self.project_root = Path(__file__).parent.parent.parent.parent
    
    def render(self):
        """Render complete biography tab."""
        self._render_header()
        self._render_photo_gallery()
        self._render_content_sections()
        self._render_interests()
        self._render_connect()
    
    def _render_header(self):
        """Render biography header."""
        header = self.content.get_dict('biography_tab.header')
        
        self.ui.bio_header(
            header.get('name', 'Dani Geiger'),
            header.get('title', 'ML Engineer & Bioinformatics Researcher'),
            header.get('tagline', 'Using AI to discover safer treatments')
        )
    
    def _render_photo_gallery(self):
        """Render photo gallery."""
        st.markdown("### 📸 Personal Gallery")
        bio_images = self.config.get('images.biography', [])
        
        if bio_images:
            cols = st.columns(len(bio_images))
            for col, img_path in zip(cols, bio_images):
                with col:
                    img_full_path = self.project_root / img_path
                    if img_full_path.exists():
                        st.image(str(img_full_path), use_column_width=True)
    
    def _render_content_sections(self):
        """Render content sections (About Me, Why CGRP)."""
        sections = self.content.get_dict('biography_tab.sections')
        
        # About Me
        about = sections.get('about_me', {})
        self.ui.bio_card(
            about.get('title', 'About Me'),
            about.get('content', ''),
            about.get('icon', '👤')
        )
        
        # Why CGRP
        why_cgrp = sections.get('why_cgrp', {})
        self.ui.bio_card(
            why_cgrp.get('title', 'Why CGRP?'),
            why_cgrp.get('content', ''),
            why_cgrp.get('icon', '💊')
        )
    
    def _render_interests(self):
        """Render research and personal interests."""
        # Research interests
        research = self.content.get_dict('biography_tab.research_interests')
        st.markdown(f"### {research.get('icon', '🔬')} {research.get('title', 'Research Interests')}")
        topics = self.content.get_list('biography_tab.research_interests.topics')
        if topics:
            self.ui.research_tags(topics)
        
        # Personal interests
        personal = self.content.get_dict('biography_tab.personal_interests')
        st.markdown(f"### {personal.get('icon', '❤️')} {personal.get('title', 'Personal Interests')}")
        hobbies = self.content.get_list('biography_tab.personal_interests.topics')
        if hobbies:
            self.ui.research_tags(hobbies)
    
    def _render_connect(self):
        """Render connect/contact section."""
        connect = self.content.get_dict('biography_tab.connect')
        links = connect.get('links', {})
        
        st.markdown("---")
        st.markdown(f"### {connect.get('icon', '🔗')} {connect.get('title', 'Connect')}")
        
        link_items = []
        for key, link_data in links.items():
            if 'url' in link_data:
                link_items.append(f"- **{link_data.get('label', key)}:** [{link_data.get('url')}]({link_data.get('url')})")
            elif 'value' in link_data:
                link_items.append(f"- **{link_data.get('label', key)}:** {link_data.get('value')}")
        
        st.markdown('\n'.join(link_items))

