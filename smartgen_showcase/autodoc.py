import inspect
import importlib
import os
import sys
import click

class AutodocGenerator:
    def __init__(self, output_dir='docs/api'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_for_module(self, module_name):
        """Generate markdown documentation for a given module name."""
        try:
            # Add current directory to path to find local modules
            sys.path.insert(0, os.getcwd())
            try:
                module = importlib.import_module(module_name)
            except ImportError:
                # Fallback: try importing with package context if direct import fails
                module = importlib.import_module(f"smartgen_showcase.{module_name}")
        except ImportError as e:
            click.secho(f"Error: Could not import module '{module_name}': {e}", fg="red")
            return

        # Replace dots with underscores for valid filename
        safe_filename = module_name.replace('.', '_')
        output_path = os.path.join(self.output_dir, f"{safe_filename}.md")
        
        md_content = f"# API Reference: `{module_name}`\n\n"
        module_doc = inspect.getdoc(module)
        md_content += f"{module_doc if module_doc else '*No module description provided.*'}\n\n"

        # Document Classes (Only those explicitly belonging to this module)
        classes = inspect.getmembers(module, inspect.isclass)
        valid_classes = [c for c in classes if c[1].__module__.startswith(module_name)]
        
        if valid_classes:
            md_content += "## Classes\n\n"
            for name, cls in valid_classes:
                md_content += self._document_class(name, cls)

        # Document Functions (Only those explicitly belonging to this module)
        functions = inspect.getmembers(module, inspect.isfunction)
        valid_functions = [f for f in functions if f[1].__module__.startswith(module_name)]
        
        if valid_functions:
            md_content += "## Functions\n\n"
            for name, func in valid_functions:
                md_content += self._document_function(name, func)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        click.secho(f"[Generated] API reference for {module_name} at {output_path}", fg="green")
        return f"api/{safe_filename}.md"

    def _document_class(self, name, cls):
        doc = f"### `class {name}`\n\n"
        cls_doc = inspect.getdoc(cls)
        doc += f"{cls_doc if cls_doc else '*No description available.*'}\n\n"
        
        methods = inspect.getmembers(cls, inspect.isfunction)
        if methods:
            doc += "**Methods:**\n\n"
            for m_name, m_func in methods:
                if not m_name.startswith('_') or m_name == '__init__':
                    try:
                        sig = inspect.signature(m_func)
                    except ValueError:
                        sig = "(...)"
                    
                    doc += f"- **`{m_name}{sig}`**\n"
                    m_doc = inspect.getdoc(m_func)
                    if m_doc:
                        indented_doc = "\n".join(f"  {line}" for line in m_doc.split("\n"))
                        doc += f"\n{indented_doc}\n\n"
                    else:
                        doc += "\n"
        doc += "---\n\n"
        return doc

    def _document_function(self, name, func):
        try:
            sig = inspect.signature(func)
        except ValueError:
            sig = "(...)"
        
        doc = f"### `def {name}{sig}`\n\n"
        f_doc = inspect.getdoc(func)
        doc += f"{f_doc if f_doc else '*No description available.*'}\n\n"
        doc += "---\n\n"
        return doc