"""
Theme Engine: A white-label ready theme system for SmartGen Docs.

This module provides a flexible theme engine that allows companies to
drop a 'theme' folder into their project to fully rebrand the documentation
site without touching the core framework code.
"""

import os
import shutil
from typing import Dict, Optional
from pathlib import Path


class ThemeEngine:
    """
    Manages themes for SmartGen Docs.
    """
    
    def __init__(self, themes_dir: str = 'smartgen_docs/themes', custom_theme_dir: Optional[str] = None):
        """
        Initialize the theme engine.
        
        Args:
            themes_dir: Directory containing built-in themes
            custom_theme_dir: Optional directory for custom themes
        """
        self.themes_dir = themes_dir
        self.custom_theme_dir = custom_theme_dir or 'theme'
        self.current_theme = None
        self.theme_config = {}
    
    def load_theme(self, theme_name: str) -> bool:
        """
        Load a theme by name.
        
        Args:
            theme_name: Name of the theme to load
        
        Returns:
            True if theme loaded successfully, False otherwise
        """
        # First, check for custom theme
        custom_path = os.path.join(self.custom_theme_dir, theme_name)
        if os.path.exists(custom_path):
            self.current_theme = custom_path
            self._load_theme_config(custom_path)
            return True
        
        # Fall back to built-in theme
        builtin_path = os.path.join(self.themes_dir, 'default', theme_name)
        if os.path.exists(builtin_path):
            self.current_theme = builtin_path
            self._load_theme_config(builtin_path)
            return True
        
        return False
    
    def _load_theme_config(self, theme_path: str) -> None:
        """
        Load theme configuration.
        
        Args:
            theme_path: Path to the theme directory
        """
        config_file = os.path.join(theme_path, 'config.yml')
        if os.path.exists(config_file):
            import yaml
            with open(config_file, 'r') as f:
                self.theme_config = yaml.safe_load(f) or {}
    
    def get_template_path(self, template_name: str) -> Optional[str]:
        """
        Get the path to a template file.
        
        Args:
            template_name: Name of the template
        
        Returns:
            Path to the template or None if not found
        """
        if not self.current_theme:
            return None
        
        template_path = os.path.join(self.current_theme, f'{template_name}.html')
        if os.path.exists(template_path):
            return template_path
        
        return None
    
    def get_static_path(self, asset_type: str) -> Optional[str]:
        """
        Get the path to static assets.
        
        Args:
            asset_type: Type of asset (css, js, images, etc.)
        
        Returns:
            Path to the asset directory or None if not found
        """
        if not self.current_theme:
            return None
        
        asset_path = os.path.join(self.current_theme, 'static', asset_type)
        if os.path.exists(asset_path):
            return asset_path
        
        return None
    
    def copy_theme_assets(self, destination: str) -> None:
        """
        Copy theme assets to the destination directory.
        
        Args:
            destination: Destination directory for assets
        """
        if not self.current_theme:
            return
        
        static_src = os.path.join(self.current_theme, 'static')
        if os.path.exists(static_src):
            static_dst = os.path.join(destination, 'static')
            if os.path.exists(static_dst):
                shutil.rmtree(static_dst)
            shutil.copytree(static_src, static_dst)
    
    def get_theme_config(self, key: str, default=None):
        """
        Get a configuration value from the theme.
        
        Args:
            key: Configuration key
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        return self.theme_config.get(key, default)
    
    def create_custom_theme_template(self, theme_name: str) -> None:
        """
        Create a template custom theme directory structure.
        
        Args:
            theme_name: Name of the theme to create
        """
        theme_path = os.path.join(self.custom_theme_dir, theme_name)
        os.makedirs(theme_path, exist_ok=True)
        
        # Create subdirectories
        os.makedirs(os.path.join(theme_path, 'static', 'css'), exist_ok=True)
        os.makedirs(os.path.join(theme_path, 'static', 'js'), exist_ok=True)
        os.makedirs(os.path.join(theme_path, 'static', 'images'), exist_ok=True)
        
        # Create template files
        self._create_template_file(os.path.join(theme_path, 'base.html'))
        self._create_template_file(os.path.join(theme_path, 'page.html'))
        
        # Create config file
        config_content = f"""# {theme_name} Theme Configuration
name: {theme_name}
description: Custom theme for SmartGen Docs

colors:
  primary: "#0052cc"
  accent: "#ff9900"
  text: "#333333"
  background: "#ffffff"

fonts:
  heading: "Roboto"
  body: "Roboto"
  code: "Roboto Mono"
"""
        with open(os.path.join(theme_path, 'config.yml'), 'w') as f:
            f.write(config_content)
    
    @staticmethod
    def _create_template_file(path: str) -> None:
        """
        Create a template placeholder file.
        
        Args:
            path: Path to the template file
        """
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write("<!-- Custom template content -->\n")


class ThemeRegistry:
    """
    Registry for managing available themes.
    """
    
    def __init__(self):
        """Initialize the theme registry."""
        self.themes: Dict[str, Dict] = {}
    
    def register_theme(self, name: str, path: str, description: str = "") -> None:
        """
        Register a theme.
        
        Args:
            name: Name of the theme
            path: Path to the theme
            description: Description of the theme
        """
        self.themes[name] = {
            'name': name,
            'path': path,
            'description': description
        }
    
    def get_theme(self, name: str) -> Optional[Dict]:
        """
        Get theme information.
        
        Args:
            name: Name of the theme
        
        Returns:
            Theme information or None if not found
        """
        return self.themes.get(name)
    
    def list_themes(self) -> list:
        """
        List all registered themes.
        
        Returns:
            List of theme names
        """
        return list(self.themes.keys())
