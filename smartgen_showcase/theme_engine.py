"""
Theme Engine: A white-label ready theme system for SmartGen Showcase.
"""

import os
import shutil
from typing import Dict, Optional
from pathlib import Path

class ThemeEngine:
    def __init__(self, themes_dir: str = 'smartgen_showcase/themes', custom_theme_dir: Optional[str] = None):
        self.themes_dir = themes_dir
        self.custom_theme_dir = custom_theme_dir or 'theme'
        self.current_theme = None
        self.theme_config = {}
    
    def load_theme(self, theme_name: str) -> bool:
        custom_path = os.path.join(self.custom_theme_dir, theme_name)
        if os.path.exists(custom_path):
            self.current_theme = custom_path
            self._load_theme_config(custom_path)
            return True
        
        builtin_path = os.path.join(self.themes_dir, 'default', theme_name)
        if os.path.exists(builtin_path):
            self.current_theme = builtin_path
            self._load_theme_config(builtin_path)
            return True
        
        return False
    
    def _load_theme_config(self, theme_path: str) -> None:
        config_file = os.path.join(theme_path, 'config.yml')
        if os.path.exists(config_file):
            import yaml
            with open(config_file, 'r') as f:
                self.theme_config = yaml.safe_load(f) or {}
    
    def get_template_path(self, template_name: str) -> Optional[str]:
        if not self.current_theme:
            return None
        template_path = os.path.join(self.current_theme, f'{template_name}.html')
        if os.path.exists(template_path):
            return template_path
        return None
    
    def get_static_path(self, asset_type: str) -> Optional[str]:
        if not self.current_theme:
            return None
        asset_path = os.path.join(self.current_theme, 'static', asset_type)
        if os.path.exists(asset_path):
            return asset_path
        return None
    
    def copy_theme_assets(self, destination: str) -> None:
        if not self.current_theme:
            return
        static_src = os.path.join(self.current_theme, 'static')
        if os.path.exists(static_src):
            static_dst = os.path.join(destination, 'static')
            if os.path.exists(static_dst):
                shutil.rmtree(static_dst)
            shutil.copytree(static_src, static_dst)
    
    def get_theme_config(self, key: str, default=None):
        return self.theme_config.get(key, default)
    
    def create_custom_theme_template(self, theme_name: str) -> None:
        theme_path = os.path.join(self.custom_theme_dir, theme_name)
        os.makedirs(theme_path, exist_ok=True)
        
        os.makedirs(os.path.join(theme_path, 'static', 'css'), exist_ok=True)
        os.makedirs(os.path.join(theme_path, 'static', 'js'), exist_ok=True)
        os.makedirs(os.path.join(theme_path, 'static', 'images'), exist_ok=True)
        
        self._create_template_file(os.path.join(theme_path, 'base.html'))
        self._create_template_file(os.path.join(theme_path, 'page.html'))
        
        config_content = f"""# {theme_name} Theme Configuration
name: {theme_name}
description: Custom theme for SmartGen Showcase

colors:
  primary: "#4A3AE3"
  accent: "#C2660D"
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
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write("<!-- Custom template content -->\n")

class ThemeRegistry:
    def __init__(self):
        self.themes: Dict[str, Dict] = {}
    
    def register_theme(self, name: str, path: str, description: str = "") -> None:
        self.themes[name] = {
            'name': name,
            'path': path,
            'description': description
        }
    
    def get_theme(self, name: str) -> Optional[Dict]:
        return self.themes.get(name)
    
    def list_themes(self) -> list:
        return list(self.themes.keys())