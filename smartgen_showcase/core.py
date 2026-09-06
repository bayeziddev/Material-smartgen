"""
Core: Main documentation builder for SmartGen Showcase.

This module handles the conversion of Markdown files to HTML pages,
using the PathResolver to ensure all links are correct across nested directories.
"""

import os
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader
from .converter import MarkdownConverter
from .path_resolver import PathResolver

class SmartGenEngine:
    """
    Builds the documentation site from Markdown files.
    """
    
    def __init__(self, config_path='smartgen.yml', site_dir='site'):
        self.config_path = config_path
        self.site_dir = site_dir
        self.config = self.load_config()
        self.docs_dir = '.'  # Updated to root directory
        self.theme_dir = os.path.join(os.path.dirname(__file__), 'themes', 'default')
        self.converter = MarkdownConverter()
        self.env = Environment(loader=FileSystemLoader(self.theme_dir))
        
        site_url = self.config.get('site_url', '')
        self.path_resolver = PathResolver(site_url=site_url)

    def load_config(self):
        if not os.path.exists(self.config_path):
            return {"site_name": "SmartGen Showcase", "nav": []}
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def process_content_files(self):
        """Build the entire documentation site."""
        if os.path.exists(self.site_dir):
            shutil.rmtree(self.site_dir)
        os.makedirs(self.site_dir)

        with open(os.path.join(self.site_dir, '.nojekyll'), 'w') as f:
            pass

        site_url = self.config.get('site_url', '')
        if site_url:
            domain = site_url.replace('https://', '').replace('http://', '').split('/')[0]
            if domain and '.' in domain and 'github.io' not in domain:
                with open(os.path.join(self.site_dir, 'CNAME'), 'w') as f:
                    f.write(domain)

        static_src = os.path.join(self.theme_dir, 'static')
        static_dst = os.path.join(self.site_dir, 'static')
        if os.path.exists(static_src):
            shutil.copytree(static_src, static_dst)
        license_src = os.path.join(self.docs_dir, 'LICENSE')
        if os.path.exists(license_src):
            shutil.copy2(license_src, os.path.join(self.site_dir, 'LICENSE'))

        nav = self.config.get('nav', [])
        self.page_sequence = []

        def flatten_nav(nav_list):
            for item in nav_list:
                if isinstance(item, dict):
                    for title, path in item.items():
                        if isinstance(path, str):
                            if not path.startswith('http'):
                                self.page_sequence.append((title, path))
                        elif isinstance(path, list):
                            flatten_nav(path)
                elif isinstance(item, str):
                    self.page_sequence.append((item, item))

        flatten_nav(nav)

        def process_nav(nav_list):
            for item in nav_list:
                if isinstance(item, dict):
                    for title, path in item.items():
                        if isinstance(path, str):
                            self.build_page(title, path)
                        elif isinstance(path, list):
                            process_nav(path)
                elif isinstance(item, str):
                    self.build_page(item, item)
                    
        process_nav(nav)

    def build_page(self, title, md_path):
        if md_path.startswith('http://') or md_path.startswith('https://'):
            return
        
        src_path = os.path.join(self.docs_dir, md_path)
        if not os.path.exists(src_path):
            print(f"Warning: File {src_path} not found.")
            return

        with open(src_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html_body = self.converter.convert(md_content)
        
        template_name = 'page_premium.html' if os.path.exists(os.path.join(self.theme_dir, 'page_premium.html')) else 'page.html'
        template = self.env.get_template(template_name)
        
        relative_path = md_path.replace('.md', '.html')
        current_depth = self.path_resolver.get_current_depth(relative_path)
        
        breadcrumbs = [
            {"title": "Home", "link": self._relative_page_link(relative_path, "index.html")},
            {"title": title, "link": os.path.basename(relative_path)}
        ]

        prev_page, next_page = None, None
        sequence = getattr(self, 'page_sequence', [])
        for i, (seq_title, seq_path) in enumerate(sequence):
            if seq_path == md_path:
                if i > 0:
                    p_title, p_path = sequence[i - 1]
                    prev_page = {"title": p_title, "link": self._relative_page_link(relative_path, p_path.replace('.md', '.html'))}
                if i < len(sequence) - 1:
                    n_title, n_path = sequence[i + 1]
                    next_page = {"title": n_title, "link": self._relative_page_link(relative_path, n_path.replace('.md', '.html'))}
                break

        output_content = template.render(
            title=title,
            content=html_body,
            config=self.config,
            nav=self.config.get('nav', []),
            current_page=md_path,
            raw_markdown=md_content,
            breadcrumbs=breadcrumbs,
            prev_page=prev_page,
            next_page=next_page,
            current_depth=current_depth,
            path_resolver=self.path_resolver,
            url_for=lambda type, filename: self._url_for(type, filename, relative_path)
        )

        dst_path = os.path.join(self.site_dir, relative_path)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(output_content)

    def _relative_page_link(self, current_page, target_page):
        current_dir = os.path.dirname(current_page) or '.'
        return os.path.relpath(target_page, current_dir).replace(os.sep, '/')

    def _url_for(self, type, filename, current_page='index.html'):
        if type == 'static':
            current_dir = os.path.dirname(current_page) or '.'
            prefix = os.path.relpath('.', current_dir).replace(os.sep, '/')
            static_root = f"{prefix}/static" if prefix != '.' else "static"
            return f"{static_root}/{filename}"
        elif type == 'page':
            return self._relative_page_link(current_page, filename)
        return filename