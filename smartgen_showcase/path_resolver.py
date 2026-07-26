"""
PathResolver: A utility for normalizing and resolving paths in SmartGen Showcase.
"""

import os
from pathlib import Path
from typing import Optional, Tuple

class PathResolver:
    """
    Resolves and normalizes paths for the SmartGen Showcase framework.
    """
    
    def __init__(self, site_url: str = "", base_path: str = ""):
        self.site_url = site_url.rstrip('/')
        self.base_path = base_path.rstrip('/') if base_path else ""
    
    def md_to_html(self, md_path: str) -> str:
        if md_path.startswith('http://') or md_path.startswith('https://'):
            return md_path
        return md_path.replace('.md', '.html')
    
    def get_relative_path(self, current_page: str, target_page: str) -> str:
        if target_page.startswith('http://') or target_page.startswith('https://'):
            return target_page
        
        current_dir = os.path.dirname(current_page)
        if current_dir:
            common = os.path.commonpath([current_dir, os.path.dirname(target_page)])
            up_count = len(Path(current_dir).relative_to(common).parts)
            relative = os.path.join(*(['..'] * up_count), target_page)
            return relative.replace('\\', '/')
        return target_page
    
    def get_absolute_path(self, page_path: str, current_depth: int = 0) -> str:
        if page_path.startswith('http://') or page_path.startswith('https://'):
            return page_path
        if page_path.startswith('/'):
            return page_path
        path = f"/{page_path}".replace('\\', '/')
        return path
    
    def resolve_static(self, asset_path: str, current_depth: int = 0) -> str:
        if asset_path.startswith('http://') or asset_path.startswith('https://'):
            return asset_path
        if current_depth == 0:
            return f"static/{asset_path}" if not asset_path.startswith('static/') else asset_path
        up_path = '/'.join(['..'] * current_depth)
        return f"{up_path}/static/{asset_path}" if not asset_path.startswith('static/') else f"{up_path}/{asset_path}"
    
    def get_breadcrumb_link(self, breadcrumb_path: str, current_depth: int = 0) -> str:
        if breadcrumb_path.startswith('http://') or breadcrumb_path.startswith('https://'):
            return breadcrumb_path
        if current_depth == 0:
            return breadcrumb_path
        up_path = '/'.join(['..'] * current_depth)
        return f"{up_path}/{breadcrumb_path}"
    
    def get_current_depth(self, page_path: str) -> int:
        if not page_path:
            return 0
        clean_path = page_path.strip('/')
        parts = clean_path.split('/')
        if clean_path.endswith('.html'):
            return len(parts) - 1 if len(parts) > 0 else 0
        return len(parts)
    
    def normalize_path(self, path: str) -> str:
        if path.startswith('http://') or path.startswith('https://'):
            return path
        normalized = str(Path(path).as_posix())
        return normalized.lstrip('./')