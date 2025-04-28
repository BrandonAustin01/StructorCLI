import os
import re
import shutil
import sys
import random
import time
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# Initialize Rich console
console = Console(width=80)

# Path to the templates folder
TEMPLATE_DIR = Path(__file__).parent / "templates"

# Safe extensions for text injection
TEXT_EXTENSIONS = {".md", ".txt", ".py", ".html", ".js", ".css"}

SUCCESS_QUOTES = [
    "🎯 Project created! Now go conquer the world!",
    "🚀 Another step toward greatness!",
    "🔥 Your project is ready. Light it up!",
    "✨ You just built the future. One folder at a time.",
    "💡 Idea scaffolded. Execution is next!",
    "🏗️ Strong foundations lead to strong empires!",
    "🧠 Great ideas start like this — nice work!",
    "🌟 It's alive! Your project has been born!",
    "📦 All packed and ready. Time to build something amazing!",
    "💥 Creation successful. Innovation unlocked!"
]

def chunk_list(lst, n):
    """Split a list into chunks of size n, padding if needed."""
    for i in range(0, len(lst), n):
        chunk = lst[i:i + n]
        while len(chunk) < n:
            chunk.append("")
        yield chunk

def format_option(index, name):
    """Format a perfectly aligned option."""
    number = f"{index:>2}."  # Pad single digits
    return f"[cyan]{number}[/cyan] {name.capitalize()}"

def get_available_templates():
    """Return a list of available templates."""
    return sorted(p.name for p in TEMPLATE_DIR.iterdir() if p.is_dir())

def sanitize_project_name(name):
    """Remove illegal characters from project name."""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

def ask_project_choice(template_choices):
    """Ask user to select a project template with clean error handling."""
    valid_choices = [str(i) for i in range(1, len(template_choices) + 1)]

    while True:
        choice = Prompt.ask(
            "👉 Choose project type",
            choices=valid_choices,
            show_choices=False
        )

        try:
            index = int(choice) - 1
            return template_choices[index]
        except (ValueError, IndexError):
            console.print("[red]❌ Invalid choice. Please select a valid number.[/red]")

def get_project_info():
    """Prompt user for project name and template choice."""
    console.rule("[bold cyan]⭐  StructorCLI  ⭐[/bold cyan]", align="center")

    while True:
        project_name = Prompt.ask("[bold cyan]📂 Enter project name[/bold cyan]").strip()
        sanitized = sanitize_project_name(project_name)

        if sanitized and sanitized == project_name:
            break
        else:
            console.print("[yellow]⚠️ Project name had illegal characters or was empty. Please try again.[/yellow]")

    template_choices = get_available_templates()
    if not template_choices:
        console.print("[red]❌ No templates found in templates/ folder.[/red]")
        sys.exit(1)

    console.rule(f"[bold green]📂 Project: {project_name}[/bold green]", align="center")

    console.print("\n💻 [bold]Select Project Type:[/bold]\n")

    options = [format_option(i, name) for i, name in enumerate(template_choices, start=1)]

    option_rows = list(chunk_list(options, 4))

    for row in option_rows:
        # Widen the slots to 30 characters each
        line = ""
        for cell in row:
            line += cell.ljust(30)  # 👈 wider breathing room
        console.print(line.rstrip())

    console.rule()

    project_type = ask_project_choice(template_choices)

    return project_name, project_type

def scaffold_project(project_name, project_type):
    """Create project directory and copy template files, with injection and progress bar."""
    project_path = Path.cwd() / project_name

    try:
        if project_path.exists():
            raise Exception(f"Project '{project_name}' already exists.")

        template_path = TEMPLATE_DIR / project_type

        # Validate template folder
        if not template_path.exists() or not any(template_path.iterdir()):
            raise Exception(f"Template '{project_type}' is missing or empty.")

        project_path.mkdir(parents=True, exist_ok=False)

        created_files = []

        # Gather all files first
        all_files = []
        for root, _, files in os.walk(template_path):
            for file in files:
                src_file = Path(root) / file
                all_files.append(src_file)

        with Progress(
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("[bold blue]{task.description}"),
            transient=True,
        ) as progress:

            task = progress.add_task("[green]Scaffolding project...", total=len(all_files))

            for src_file in all_files:
                relative_root = src_file.parent.relative_to(template_path)
                target_dir = project_path / relative_root
                target_dir.mkdir(parents=True, exist_ok=True)

                dst_file = target_dir / src_file.name
                shutil.copy2(src_file, dst_file)
                created_files.append(dst_file)

                # Inject project name into safe text files
                if dst_file.suffix.lower() in TEXT_EXTENSIONS:
                    try:
                        text = dst_file.read_text(encoding="utf-8")
                        if "{{project_name}}" in text:
                            text = text.replace("{{project_name}}", project_name)
                            dst_file.write_text(text, encoding="utf-8")
                    except Exception as e:
                        console.print(f"[yellow]⚠️ Warning: Could not inject into {dst_file.name}: {e}[/yellow]")

                progress.update(task, advance=1)

        return project_path, created_files

    except Exception as e:
        if project_path.exists():
            shutil.rmtree(project_path, ignore_errors=True)
        raise e

def show_success(project_path, created_files):
    """Display summary table and folder tree."""
    console.print(f"\n[green]✅ Project '{project_path.name}' created successfully![/green]\n")

    table = Table(title="📄 Created Files", show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan")
    table.add_column("Size (KB)", style="green", justify="right")

    for file in created_files:
        size_kb = f"{file.stat().st_size / 1024:.2f}"
        table.add_row(str(file.relative_to(project_path.parent)), size_kb)

    console.print(table)

    tree = Tree(f"📂 {project_path.name}")

    def add_to_tree(base: Path, parent: Tree):
        for item in sorted(base.iterdir()):
            if item.is_dir():
                branch = parent.add(f"📂 {item.name}")
                add_to_tree(item, branch)
            else:
                parent.add(f"📄 {item.name}")

    add_to_tree(project_path, tree)

    console.print(tree)

def main():
    """Main CLI entry point with retry loop."""
    while True:
        try:
            project_name, project_type = get_project_info()
            project_path, created_files = scaffold_project(project_name, project_type)
            show_success(project_path, created_files)

            success_message = random.choice(SUCCESS_QUOTES)
            console.print(f"\n[bold green]{success_message}[/bold green]\n")

            break

        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]\n")

            choice = Prompt.ask(
                "[yellow]Would you like to try again?[/yellow]",
                choices=["y", "n"],
                show_choices=False
            )
            if choice.lower() != "y":
                console.print("[bold red]👋 Exiting. Goodbye.[/bold red]")
                sys.exit(0)
