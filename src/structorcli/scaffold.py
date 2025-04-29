# ====== Standard Library Imports ======
import os
import re
import shutil
import sys
import random
import time
from pathlib import Path

# ====== Rich Library Imports for Better CLI UI ======
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# ====== Initialize Rich Console ======
# Rich is used to improve output in the terminal with colors, layout, and animation
console = Console(width=120)

# ====== Configuration ======
# This folder should contain one subfolder per template (e.g., "flask", "node", "react")
TEMPLATE_DIR = Path(__file__).parent / "templates"

# Define file types we allow text injection into (e.g., inserting the project name)
TEXT_EXTENSIONS = {".md", ".txt", ".py", ".html", ".js", ".css", ".json"}

# Fun success messages to randomly choose from when the project is scaffolded
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
    "💥 Creation successful. Innovation unlocked!",
    "🧰 Template deployed. Time to innovate.",
    "🔧 Your tools are set. Go build magic.",
    "🧬 Project initialized. Evolution begins now.",
    "💻 Codebase scaffolded — welcome to your new workspace.",
    "🦾 Automation complete. You’re unstoppable.",
    "🚧 Framework set. It’s all yours from here.",
    "🌀 Structure dropped like a pro.",
    "🧪 System online. Begin your experiment.",
    "🎉 Files generated. Now let the fun begin!",
    "🔭 Your vision is no longer abstract.",
    "📐 Precision scaffolding: 100%.",
    "⚙️ The engine is primed. Start coding.",
    "🧱 Foundation built. Stack your ideas next.",
    "🎮 Dev mode activated. Let’s play.",
    "💼 Project unpacked — now make it yours.",
    "🎯 Precision achieved. Now go break the rules.",
    "⚡️ All systems nominal. Engage dev mode.",
    "🗺️ Map drawn. Adventure awaits.",
    "👨‍🚀 Launch sequence complete. Welcome to your codebase.",
    "🛠️ Project wired up — you're in control now.",
    "🔒 Vault opened. Secrets of structure revealed.",
    "💡 Idea manifested. Now make it legendary.",
    "📀 Code written in stone. Now etch your legacy.",
    "🎛️ Engine compiled. Drive it like you stole it.",
    "🛸 Structure landed. We are not alone.",
    "🧠 Another brainchild is born. Raise it well.",
    "📣 Hey, it actually worked. What a concept.",
    "🤖 StructorCLI has done its duty. Don’t mess it up.",
    "🥽 Project deployed. May the bugs fear you.",
    "🎨 Canvas stretched. Now splash your genius.",
    "📈 Your build stats just got better looking.",
    "🪄 That was basically magic. Don’t question it.",
    "🌪️ Code whirlwind complete. Time to calm the chaos.",
    "💣 Deployed like a dev ninja. No trace left.",
    "🧩 The pieces are in place. Play the game.",
    "🧯 Build complete. Fire up the creativity.",
    "🗜️ Project compressed, deployed, and awesome-fied.",
    "🎯 Bullseye hit. Now fill it with substance.",
    "📡 Signal locked. Commence collaboration.",
    "🥷 Structor strikes again. Silently efficient.",
    "📸 Snapshot taken. Let’s see what you can do.",
    "💾 Saved your time, saved your brain. You're welcome.",
    "🐍 Python’d. Bashed. React’d. Compiled. You’re ready.",
    "🌍 World-class structure created. From your terminal."
]

# ====== Utility Functions ======

def animated_typing(text, delay=0.04, style="bold green"):
    """Print text character-by-character for a typewriter effect."""
    for char in text:
        console.print(char, style=style, end="")
        time.sleep(delay)
    console.print()  # move to next line

def chunk_list(lst, n):
    """Split a list into fixed-size chunks (used to layout template names in columns)."""
    for i in range(0, len(lst), n):
        chunk = lst[i:i + n]
        while len(chunk) < n:
            chunk.append("")
        yield chunk

def format_option(index, name):
    """Return a formatted CLI menu option string with index and name."""
    number = f"{index:>2}."  # Right-align numbers to make menu look nice
    return f"[cyan]{number}[/cyan] {name.capitalize()}"

def get_available_templates():
    """List all folders in the templates directory."""
    return sorted(p.name for p in TEMPLATE_DIR.iterdir() if p.is_dir())

def sanitize_project_name(name):
    """Clean the project name by removing characters that are illegal in filenames."""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

def ask_project_choice(template_choices):
    """Display template options and safely get user selection."""
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
    """Prompt for project name and template selection."""
    console.rule("[bold cyan]⭐  StructorCLI  ⭐[/bold cyan]", align="center")

    # Ask for project name, sanitizing bad characters
    while True:
        project_name = Prompt.ask("[bold cyan]📂 Enter project name[/bold cyan]").strip()
        sanitized = sanitize_project_name(project_name)

        if sanitized and sanitized == project_name:
            break
        else:
            console.print("[yellow]⚠️ Project name had illegal characters or was empty. Please try again.[/yellow]")

    # Load templates from the local 'templates/' folder
    template_choices = get_available_templates()
    if not template_choices:
        console.print("[red]❌ No templates found in templates/ folder.[/red]")
        sys.exit(1)

    console.rule(f"[bold green]📂 Project: {project_name}[/bold green]", align="center")

    # Display templates in multiple columns
    console.print("\n💻 [bold]Select Project Type:[/bold]\n")
    num_columns = 4
    rows = (len(template_choices) + num_columns - 1) // num_columns

    for row in range(rows):
        line = ""
        for col in range(num_columns):
            idx = col * rows + row
            if idx < len(template_choices):
                name = template_choices[idx].capitalize()
                line += f"{idx+1:2}. {name:<30}"  # Fixed width columns
        console.print(line.rstrip())

    console.rule()

    # Ask for user selection
    project_type = ask_project_choice(template_choices)

    return project_name, project_type

def scaffold_project(project_name, project_type):
    """
    Create a new project directory and populate it using a selected template.
    It also replaces placeholder variables like {{project_name}} in supported files.
    """
    project_path = Path.cwd() / project_name

    try:
        if project_path.exists():
            raise Exception(f"Project '{project_name}' already exists.")

        template_path = TEMPLATE_DIR / project_type

        # Check template exists and is not empty
        if not template_path.exists() or not any(template_path.iterdir()):
            raise Exception(f"Template '{project_type}' is missing or empty.")

        project_path.mkdir(parents=True, exist_ok=False)
        created_files = []

        # Collect all files to scaffold
        all_files = []
        for root, _, files in os.walk(template_path):
            for file in files:
                src_file = Path(root) / file
                all_files.append(src_file)

        # Create a progress bar for copying files
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

                # Replace placeholder with actual project name in supported text files
                if dst_file.suffix.lower() in TEXT_EXTENSIONS:
                    try:
                        text = dst_file.read_text(encoding="utf-8")
                        if "{{project_name}}" in text:
                            text = text.replace("{{project_name}}", project_name)
                            dst_file.write_text(text, encoding="utf-8")
                    except Exception as e:
                        console.print(f"[yellow]⚠️ Could not inject into {dst_file.name}: {e}[/yellow]")

                progress.update(task, advance=1)
                time.sleep(0.2)  # Optional: simulate progress

        return project_path, created_files

    except Exception as e:
        # Cleanup if something went wrong
        if project_path.exists():
            shutil.rmtree(project_path, ignore_errors=True)
        raise e

def show_success(project_path, created_files):
    """Print a summary of created files and a folder tree view."""
    console.print(f"\n[green]✅ Project '{project_path.name}' created successfully![/green]\n")

    # Show table of all created files
    table = Table(title="📄 Created Files", show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan")
    table.add_column("Size (KB)", style="green", justify="right")

    for file in created_files:
        size_kb = f"{file.stat().st_size / 1024:.2f}"
        table.add_row(str(file.relative_to(project_path.parent)), size_kb)

    console.print(table)

    # Show visual tree of the new folder
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
    """Main entry point of the StructorCLI tool. Handles retries and errors gracefully."""
    while True:
        try:
            project_name, project_type = get_project_info()
            project_path, created_files = scaffold_project(project_name, project_type)
            show_success(project_path, created_files)

            success_message = random.choice(SUCCESS_QUOTES)
            console.print()
            animated_typing(success_message)
            console.print()
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