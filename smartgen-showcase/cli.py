import click
import os
from .core import SmartGenEngine
from .server import DevServer
from .autodoc import AutodocGenerator
from .scaffold import Scaffolder
from .changelog_renderer import ChangelogRenderer

@click.group()
def main():
    """SmartGen Showcase - A premium portfolio & design platform by Sayad Md Bayezid Hosan."""
    pass

@main.command()
@click.option('--config', default='smartgen.yml', help='Path to config file.')
@click.option('--site-dir', default='site', help='Directory to output the built site.')
def build(config, site_dir):
    """Build the showcase site."""
    if not os.path.exists(config):
        click.secho(f"Error: Config file '{config}' not found. Run 'smartgen-showcase init' first.", fg="red")
        return
    
    click.secho(f"Building showcase using {config}...", fg="cyan")
    engine = SmartGenEngine(config)
    engine.process_content_files()
    click.secho(f"Successfully built showcase to '{site_dir}'.", fg="green", bold=True)

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
    click.echo("Open your browser to manage and upload design/showcase files.")
    try:
        from .upload_server import app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
    except ImportError:
        click.secho("Error: FastAPI is not installed. Install it with: pip install fastapi uvicorn", fg="red")

@main.command()
@click.option('--config', default='smartgen.yml', help='Path to config file.')
def scaffold(config):
    """Auto-generate missing content files and folders safely from config."""
    click.secho("Starting scaffolding process...", fg="cyan")
    scaffolder = Scaffolder(config)
    scaffolder.create_files()

@main.command()
@click.argument('module_name')
@click.option('--output', default='showcase/api', help='Directory to save reference files.')
def autodoc(module_name, output):
    """Generate reference docs from Python module."""
    click.secho(f"Generating reference for {module_name}...", fg="cyan")
    generator = AutodocGenerator(output)
    generator.generate_for_module(module_name)
    click.secho("Reference documentation generated successfully.", fg="green")

@main.command()
@click.option('--json-path', default='data/changelog.json', help='Path to changelog JSON.')
@click.option('--output', default='changelog.md', help='Output Markdown file.')
def render_changelog(json_path, output):
    """Render changelog.json into a Markdown file for the showcase."""
    click.secho("Rendering changelog from JSON...", fg="cyan")
    renderer = ChangelogRenderer(json_path, output)
    renderer.render()

@main.command()
def init():
    """Initialize a new SmartGen Showcase project."""
    if os.path.exists('smartgen.yml'):
        click.secho("Error: smartgen.yml already exists in this directory.", fg="red")
        return
    
    # Create the premium showcase boilerplate config
    config_content = """# SmartGen Showcase Configuration
site_name: SmartGen Design Showcase
site_url: https://github.com/bayeziddev/Material-smartgen
site_author: Sayad Md Bayezid Hosan

theme:
  name: premium
  palette:
    primary: "#4A3AE3"
    accent: "#C2660D"

nav:
  - Home: index.md
  - Showcase:
      - Gallery: showcase/index.md
"""
    with open('smartgen.yml', 'w') as f:
        f.write(config_content)
    
    # Scaffold directories
    os.makedirs('showcase', exist_ok=True)
    
    # Create default markdown files
    with open('index.md', 'w') as f:
        f.write("# Welcome to SmartGen Showcase\n\nThis portfolio site was built by **Sayad Md Bayezid Hosan**.\n\nEdit this file in `index.md` to get started.\n")
        
    with open('showcase/index.md', 'w') as f:
        f.write("# Showcase Gallery\n\nExplore templates and design assets. Run `smartgen-showcase serve` to see your changes live!\n")
    
    click.secho("Showcase project initialized successfully!", fg="green", bold=True)
    click.echo("Run ", nl=False)
    click.secho("smartgen-showcase serve", fg="cyan", bold=True, nl=False)
    click.echo(" to see it in action.")

if __name__ == "__main__":
    main()