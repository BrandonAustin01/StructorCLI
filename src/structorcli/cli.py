# ====== Standard Library Imports ======
import sys
import random

# ====== Rich for CLI UI Enhancements ======
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# ====== Used for version retrieval ======
from importlib.metadata import version, PackageNotFoundError

# ====== Import the main scaffold logic ======
from structorcli.scaffold import main, get_available_templates

# ====== Initialize the Rich console for styled CLI output ======
console = Console()

# ================================
# 📋 CLI OPTION HANDLERS
# ================================

def show_list():
    """Print a table of all available templates inside templates/."""
    templates = get_available_templates()
    table = Table(title="📁 Available Templates", show_header=False, box=None, padding=(0, 2))

    for i, name in enumerate(templates, start=1):
        table.add_row(f"[cyan]{i:2}.[/cyan]", f"[white]{name.capitalize()}[/white]")

    console.print(table)

def show_help():
    """Display usage instructions and available CLI options."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    ver = version("structorcli")

    table.add_row("Usage:", "[bold cyan]structor[/] [options]")
    table.add_row("Version:", f"[bold green] {ver} [/]")
    table.add_row("", "")
    table.add_row("Options:", "")
    table.add_row("[green]--help[/], [green]-h[/]", "Show this help message")
    table.add_row("[green]--version[/], [green]-v[/]", "Show the current version")
    table.add_row("[green]--list[/], [green]-l[/], [green]list[/]", "List available templates")
    table.add_row("[green]--template <name>[/]", "Scaffold using a specific template")
    table.add_row("[green]--name <project>[/]", "Set project name (used with --template)")
    table.add_row("[green]--quiet[/], [green]-q[/]", "Suppress quotes and non-essential output")
    table.add_row("", "")
    table.add_row("Description:", "Interactive scaffolder for modern project bootstraps.")
    table.add_row("Author:", "[bold blue]Brandon McKinney[/bold blue]")

    console.print(Panel(table, title="[bold]⭐  StructorCLI  ⭐[/bold]", border_style="cyan", expand=False))

def show_version():
    """Display the installed version of StructorCLI (from PyPI or fallback to dev)."""
    try:
        ver = version("structorcli")
        console.print(f"[bold green]StructorCLI[/bold green] version [bold cyan]{ver}[/bold cyan]")
    except PackageNotFoundError:
        console.print("[bold yellow]StructorCLI[/bold yellow] (local dev version)")

# ================================
# 🚀 MAIN CLI ENTRY LOGIC
# ================================

def run():
    """Primary entry point for the CLI command (e.g., when running 'structor')."""
    args = sys.argv[1:]
    quiet_mode = "--quiet" in args or "-q" in args

    # --- Handle --help ---
    if "--help" in args or "-h" in args:
        show_help()
        return

    # --- Handle --version ---
    if "--version" in args or "-v" in args:
        show_version()
        return

    # --- Handle --list or list ---
    if "list" in args or "--list" in args or "-l" in args:
        show_list()
        return

    # --- Handle direct scaffold from args ---
    if "--template" in args:
        try:
            template_index = args.index("--template") + 1
            template_name = args[template_index]
        except IndexError:
            console.print("[red]❌ Missing template name after --template[/red]")
            return

        # Re-importing here to avoid unnecessary import cost unless --template is used
        from structorcli.scaffold import (
            scaffold_project,
            show_success,
            get_available_templates,
            sanitize_project_name,
            SUCCESS_QUOTES
        )

        templates = get_available_templates()
        if template_name.lower() not in templates:
            console.print(f"[red]❌ Template '{template_name}' not found.[/red]")
            return

        # Optional: Handle --name argument
        if "--name" in args:
            try:
                name_index = args.index("--name") + 1
                project_name = args[name_index]
            except IndexError:
                console.print("[red]❌ Missing project name after --name[/red]")
                return
        else:
            # Prompt user if --name not provided
            project_name = Prompt.ask("[cyan]📂 Enter project name[/cyan]").strip()

        project_name = sanitize_project_name(project_name)
        if not project_name:
            console.print("[red]❌ Invalid project name.[/red]")
            return

        # Create the project from template
        try:
            project_path, created_files = scaffold_project(project_name, template_name)
            show_success(project_path, created_files)
            if not quiet_mode:
                console.print()
                console.print(f"[bold green]{random.choice(SUCCESS_QUOTES)}[/bold green]\n")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
        return

    # --- Default Interactive Mode ---
    from structorcli.scaffold import main
    try:
        project_name, project_type = main()
        if not quiet_mode:
            from structorcli.scaffold import SUCCESS_QUOTES
            console.print()
            console.print(f"[bold green]{random.choice(SUCCESS_QUOTES)}[/bold green]\n")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


# Run the CLI if the file is executed directly
if __name__ == "__main__":
    run()
