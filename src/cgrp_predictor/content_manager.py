"""
Content Management Module
==========================

Centralized content management for separation of content from code.
Loads all user-facing text from YAML configuration for easy editing.

Author: Dani Geiger
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class ContentManager:
    """
    Professional content management system.
    
    Loads and manages all user-facing text content from YAML files,
    enabling non-developers to edit content without touching code.
    
    Best Practices:
    - Separation of content from code
    - Easy content updates
    - Multi-language support ready
    - Version-controlled content
    
    Example:
        >>> content = ContentManager()
        >>> title = content.get('app.title')
        >>> steps = content.get_steps('predictor_tab.info_sections.how_it_works.steps')
    """
    
    _instance: Optional['ContentManager'] = None
    _content: Optional[Dict[str, Any]] = None
    
    def __new__(cls, content_path: Optional[str] = None):
        """
        Implement singleton pattern for content management.
        
        Args:
            content_path: Path to content YAML file
            
        Returns:
            ContentManager: Singleton instance
        """
        if cls._instance is None:
            cls._instance = super(ContentManager, cls).__new__(cls)
            cls._instance._initialize(content_path)
        return cls._instance
    
    def _initialize(self, content_path: Optional[str] = None) -> None:
        """
        Initialize content from YAML file.
        
        Args:
            content_path: Path to content YAML file
        """
        if content_path is None:
            project_root = Path(__file__).parent.parent.parent
            content_path = project_root / "config" / "content.yaml"
        else:
            content_path = Path(content_path)
        
        if not content_path.exists():
            logger.warning(f"Content file not found: {content_path}, using defaults")
            self._content = {}
            return
        
        try:
            with open(content_path, 'r') as f:
                self._content = yaml.safe_load(f)
            logger.info(f"Content loaded from {content_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing content file: {e}")
            self._content = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get content value by dot-notation key.
        
        Args:
            key: Content key in dot notation
            default: Default value if not found
            
        Returns:
            Content value or default
        """
        keys = key.split('.')
        value = self._content
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def format_message(self, key: str, **kwargs) -> str:
        """
        Get formatted message with variable substitution.
        
        Args:
            key: Message key
            **kwargs: Variables to substitute
            
        Returns:
            str: Formatted message
            
        Example:
            >>> content.format_message('messages.success.loaded_molecules', count=20)
            'Successfully loaded 20 molecules'
        """
        message = self.get(key, "")
        try:
            return message.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing variable in message template: {e}")
            return message
    
    def get_list(self, key: str) -> List[str]:
        """
        Get list content.
        
        Args:
            key: Content key for list
            
        Returns:
            List of strings
        """
        value = self.get(key, [])
        return value if isinstance(value, list) else []
    
    def get_dict(self, key: str) -> Dict[str, Any]:
        """
        Get dictionary content.
        
        Args:
            key: Content key for dict
            
        Returns:
            Dictionary
        """
        value = self.get(key, {})
        return value if isinstance(value, dict) else {}


class TemplateRenderer:
    """
    HTML template rendering with content injection.
    
    Renders reusable HTML templates with content from ContentManager.
    Follows separation of concerns for maintainability.
    """
    
    def __init__(self, content_manager: ContentManager):
        """
        Initialize template renderer.
        
        Args:
            content_manager: ContentManager instance
        """
        self.content = content_manager
    
    def render_metric_card(
        self,
        title: str,
        value: str,
        subtitle: str = "",
        center: bool = False,
        border_color: str = "#1f77b4"
    ) -> str:
        """
        Render metric card HTML.
        
        Args:
            title: Card title
            value: Main value to display
            subtitle: Optional subtitle
            center: Whether to center text
            border_color: Left border color
            
        Returns:
            str: HTML for metric card
        """
        text_align = "text-align: center;" if center else ""
        subtitle_html = f'<p style="color: #6c757d; font-size: 0.9rem; margin: 0.5rem 0;">{subtitle}</p>' if subtitle else ""
        
        return f"""
        <div class="metric-card" style="{text_align} border-left-color: {border_color};">
            <h4 style="color: #6c757d; margin: 0;">{title}</h4>
            <h1 style="color: {border_color}; margin: 0.5rem 0;">{value}</h1>
            {subtitle_html}
        </div>
        """
    
    def render_classification_box(
        self,
        classification_key: str
    ) -> str:
        """
        Render classification guide box.
        
        Args:
            classification_key: Key in content for classification
                              (e.g., 'predictor_tab.ic50_interpretation.classifications.active')
            
        Returns:
            str: HTML for classification box
        """
        data = self.content.get_dict(classification_key)
        
        return f"""
        <div style="background: {data.get('background', '#fff')}; 
                    padding: 1.5rem; 
                    border-radius: 10px; 
                    text-align: center; 
                    border: 2px solid {data.get('border', '#ccc')};">
            <h2 style="color: {data.get('border', '#000')}; margin: 0;">
                {data.get('emoji', '')} {data.get('name', '')}
            </h2>
            <h3 style="color: {data.get('text_color', '#000')}; margin: 0.5rem 0;">
                {data.get('threshold', '')}
            </h3>
            <p style="color: {data.get('text_color', '#000')}; margin: 0;">
                <strong>{data.get('description', '')}</strong>
            </p>
            <p style="color: #6c757d; font-size: 0.9rem;">
                {data.get('detail', '')}
            </p>
        </div>
        """
    
    def render_info_card(
        self,
        title: str,
        content: str,
        icon: str = "📝"
    ) -> str:
        """
        Render biography/info card HTML.
        
        Args:
            title: Card title
            content: Card content (HTML allowed)
            icon: Emoji icon
            
        Returns:
            str: HTML for info card
        """
        return f"""
        <div class="bio-card">
            <h2 style="color: #1f77b4; margin-top: 0;">{icon} {title}</h2>
            <div style="line-height: 1.8; color: #2c3e50;">{content}</div>
        </div>
        """
    
    def render_header(
        self,
        name: str,
        title: str,
        tagline: str
    ) -> str:
        """
        Render biography header HTML.
        
        Args:
            name: Person's name
            title: Professional title
            tagline: Tagline/motto
            
        Returns:
            str: HTML for header
        """
        return f"""
        <div class="bio-header">
            <h1 style="color: white; border: none; margin: 0;">{name}</h1>
            <h3 style="color: rgba(255,255,255,0.9); margin: 0.5rem 0;">{title}</h3>
            <p style="font-size: 1.1rem; color: rgba(255,255,255,0.8); margin-top: 1rem;">
                {tagline}
            </p>
        </div>
        """

