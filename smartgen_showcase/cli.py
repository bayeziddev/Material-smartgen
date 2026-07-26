import click
import os
from .core import SmartGenEngine
from .server import DevServer
from .autodoc import AutodocGenerator
from .scaffold import Scaffolder
from .changelog_renderer import ChangelogRenderer

@click.group()
def main():
    """SmartGen Showcase - A premium portfolio platform."""
    pass

@main.command()
@click.option('--config', default='smartgen.yml', help='Path to config file.')
@click.option('--site-dir', default='site', help='Directory to output the built site.')
def build(config, site_dir):
    """Build the documentation site."""
    if not os.path.exists(config):
        click.secho(f"Error: Config file '{config}' not found. Run 'smartgen-showcase init' first.", fg="red")
        return
    
    click.secho(f"Building site using {config}...", fg="cyan")
    engine = SmartGenEngine(config, site_dir)
    engine.process_content_files()
    click.secho(f"Successfully built site to '{site_dir}'.", fg="green", bold=True)

@main.command()
@click.option('--config', default='smartgen.yml', help='Path to config file.')
@click.option('--port', default=8000, help='Port to serve on.')
def serve(config, port):
    """Start the development server with live reload."""
    if not os.path.exists(config):
        click.secho(f"Error: Config file '{config}' not found. Run 'smartgen-showcase init' first.", fg="red")
        return
    
    click.secho(f"Starting dev server on http://localhost:{port}...", fg="cyan")
    server = DevServer(config, port)
    server.run()

@main.command()
@click.option('--port', default=8001, help='Port to serve the upload manager on.')
def upload_manager(port):
    """Start the web-based upload and management interface."""
    click.secho(f"Starting upload manager on http://localhost:{port}", fg="cyan")
    click.echo("Open your browser to manage and upload documentation files.")
    try:
        from .upload_server import app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
    except ImportError:
        click.secho("Error: FastAPI is not installed. Install it with: pip install fastapi uvicorn", fg="red")

@main.command()
@click.option('--config', default='smartgen.yml', help='Path to config file.')
def scaffold(config):
    """Auto-generate missing markdown files and folders safely from config."""
    click.secho("Starting scaffolding process...", fg="cyan")
    scaffolder = Scaffolder(config)
    scaffolder.create_files()

@main.command()
@click.argument('module_name')
@click.option('--output', default='docs/api', help='Directory to save API docs.')
def autodoc(module_name, output):
    """Generate API reference from Python module."""
    click.secho(f"Generating API reference for {module_name}...", fg="cyan")
    generator = AutodocGenerator(output)
    generator.generate_for_module(module_name)
    click.secho("API documentation generated successfully.", fg="green")

@main.command()
@click.option('--json-path', default='data/changelog.json', help='Path to changelog JSON.')
@click.option('--output', default='docs/changelog.md', help='Output Markdown file.')
def render_changelog(json_path, output):
    """Render changelog.json into a Markdown file for the docs."""
    click.secho("Rendering changelog from JSON...", fg="cyan")
    renderer = ChangelogRenderer(json_path, output)
    renderer.render()

@main.command()
def init():
    """Initialize a new SmartGen Showcase project."""
    if os.path.exists('smartgen.yml'):
        click.secho("Error: smartgen.yml already exists in this directory.", fg="red")
        return
    
    config_content = """# SmartGen Showcase Configuration
site_name: My SmartGen Showcase
site_url: https://github.com/bayeziddev/smartGenShowcase
site_author: Sayad Md Bayezid Hosan

theme:
  name: premium
  palette:
    primary: "#0052cc"
    accent: "#ff9900"

nav:
  - Home: index.md
"""
    with open('smartgen.yml', 'w') as f:
        f.write(config_content)
        
    with open('index.md', 'w') as f:
        f.write("# Welcome to SmartGen Showcase\n\nRun `smartgen-showcase serve` to see your changes live!\n")
    
    click.secho("Project initialized successfully!", fg="green", bold=True)

if __name__ == "__main__":
    main()