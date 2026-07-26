import json
import os
import re
import click

class ChangelogRenderer:
    def __init__(self, json_path='data/changelog.json', output_path='changelog.md'):
        self.json_path = json_path
        self.output_path = output_path
        self.stop_words = {
            'this', 'that', 'with', 'from', 'your', 'have', 'more', 'will', 
            'into', 'been', 'were', 'also', 'their', 'then', 'than', 'could', 
            'should', 'would', 'these', 'those', 'which', 'when', 'what', 'where',
            'update', 'fixed', 'added', 'removed', 'changed', 'docs', 'file', 'code'
        }

    def _extract_seo_keywords(self, text, files):
        combined_text = f"{text} {' '.join(files)}".lower()
        words = re.findall(r'\b[a-zA-Z]{4,}\b', combined_text)
        keywords = [w for w in words if w not in self.stop_words]
        unique_keywords = list(dict.fromkeys(keywords))[:5]
        return unique_keywords if unique_keywords else ["smartgen", "update", "system"]

    def _analyze_commit_intent(self, title, description, changed_files):
        weak_titles = ['update', 'fix', 'bug', 'test', 'wip', 'changes', 'auto', 'docs(changelog)', 'skip ci']
        is_weak_title = len(title) < 8 or any(w in title.lower() for w in weak_titles)
        is_weak_desc = not description or description.strip() == "Platform improvements and optimizations." or description == title

        if not changed_files:
            return title, description

        categories = {'core': 0, 'docs': 0, 'config': 0, 'ui': 0}
        file_names = [os.path.basename(f) for f in changed_files if isinstance(f, str)]
        file_list_str = ", ".join([f"`{f}`" for f in file_names[:3]])
        if len(file_names) > 3:
            file_list_str += " and others"

        for f in changed_files:
            if not isinstance(f, str): continue
            if f.endswith('.py'): categories['core'] += 1
            elif f.endswith('.md'): categories['docs'] += 1
            elif f.endswith(('.yml', '.yaml', '.json')): categories['config'] += 1
            elif f.endswith(('.html', '.css', '.js', '.png', '.jpg')): categories['ui'] += 1

        dominant = max(categories, key=categories.get)

        auto_title = title
        auto_desc = description

        if is_weak_title:
            if dominant == 'core' and categories['core'] > 0: auto_title = "Backend Logic & Core System Engine Update"
            elif dominant == 'docs' and categories['docs'] > 0: auto_title = "Showcase Content & Structure Refinements"
            elif dominant == 'ui' and categories['ui'] > 0: auto_title = "Theme, UI & Frontend Template Adjustments"
            elif dominant == 'config' and categories['config'] > 0: auto_title = "System Configuration & Workflow Updates"
            else: auto_title = "General Platform Maintenance & Sync"

        if is_weak_desc:
            if dominant == 'core': auto_desc = f"Automated system analysis indicates architectural modifications primarily affecting {file_list_str}."
            elif dominant == 'docs': auto_desc = f"Content updates applied to {file_list_str} to improve presentation and overall accuracy."
            elif dominant == 'ui': auto_desc = f"Visual and structural template modifications applied to {file_list_str} to improve user experience."
            elif dominant == 'config': auto_desc = f"Environment variables, settings, or data structures adjusted in {file_list_str}."
            else: auto_desc = f"Routine updates, file tracking, and general maintenance applied primarily to {file_list_str}."

        return auto_title, auto_desc

    def render(self):
        if not os.path.exists(self.json_path):
            click.secho(f"Error: {self.json_path} not found.", fg="red")
            return

        with open(self.json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                click.secho(f"Error: Invalid JSON in {self.json_path}", fg="red")
                return

        if not data:
            click.secho("Changelog data is empty. Skipping render.", fg="yellow")
            return

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        md_content = "---\n"
        md_content += "title: SmartGen Platform Changelog\n"
        md_content += "description: Stay up-to-date with the latest features, bug fixes, and system enhancements.\n"
        md_content += "keywords: smartgen, changelog, showcase, updates, developer tools\n"
        md_content += "---\n\n"
        
        md_content += "# 📝 SmartGen Changelog\n\n"

        for entry in data:
            original_title = entry.get('title', '')
            original_desc = entry.get('description', '')
            changed_files = entry.get('changed_files', [])
            
            title, description = self._analyze_commit_intent(original_title, original_desc, changed_files)
            
            date_full = entry.get('date', '')
            author = entry.get('author', 'SmartGen Bot')
            short_commit = entry.get('short_commit', '')
            commit_url = entry.get('commit_url', '#')
            
            files_changed_count = entry.get('files_changed', 0)
            insertions = entry.get('insertions', 0)
            deletions = entry.get('deletions', 0)

            keywords = self._extract_seo_keywords(title + " " + description, changed_files)
            formatted_keywords = ", ".join([f"`{k}`" for k in keywords])

            date_clean = date_full.split('T')[0] if 'T' in date_full else date_full

            md_content += f"## 🚀 {date_clean} - {title}\n\n"
            md_content += f"**🎯 Impact Summary:** This update modified `{files_changed_count}` files, resulting in `{insertions}` new additions and `{deletions}` deletions.\n\n"
            
            md_content += f"- **👤 Author:** {author}\n"
            md_content += f"- **🔗 Commit:** [{short_commit}]({commit_url})\n"
            md_content += f"- **🔍 SEO Keywords:** {formatted_keywords}\n"
            
            if description and description.strip():
                desc_clean = description.strip().replace('\n', ' ')
                md_content += f"- **💡 System Note:** {desc_clean}\n"
            
            md_content += "\n---\n\n"

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        click.secho(f"[Generated] Smart SEO-Optimized Changelog rendered at {self.output_path}", fg="green")