import argparse
import logging
import shlex
import sys
from classroom import Classroom
from rich.console import Console
from rich.table import Table

def handle_command(command, name=None):
    """Handles the command execution."""
    console = Console()
    classroom = Classroom()

    if command == "add-student":
        if not name:
            console.print("[red]Error: The 'add-student' command requires a name.[/red]")
            return
        if classroom.add_student(name):
            console.print(f"[green]Student '{name}' added.[/green]")
        else:
            console.print(f"[yellow]Student '{name}' already exists.[/yellow]")
    elif command == "list-students":
        students = classroom.list_students()
        if students:
            table = Table(title="Students")
            table.add_column("Name", style="cyan")
            for student in students:
                table.add_row(student)
            console.print(table)
        else:
            console.print("[yellow]No students in the classroom.[/yellow]")
    elif command == "remove-student":
        if not name:
            console.print("[red]Error: The 'remove-student' command requires a name.[/red]")
            return
        if classroom.remove_student(name):
            console.print(f"[green]Student '{name}' removed.[/green]")
        else:
            console.print(f"[red]Student '{name}' not found.[/red]")

def setup_logging():
    """Sets up logging to a file."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="interactive.log",
        filemode="a"
    )

def interactive_mode():
    """Starts an interactive session for classroom management."""
    setup_logging()
    logging.info("Interactive session started.")
    console = Console()
    console.print("[bold cyan]Welcome to the Interactive Classroom Management System![/bold cyan]")
    console.print("Type 'help' for a list of commands, or 'exit' to quit.")

    while True:
        try:
            user_input = console.input("[bold yellow]>>> [/bold yellow]").strip()
            if not user_input:
                continue

            logging.info(f"User input: {user_input}")

            parts = shlex.split(user_input)
            if not parts:
                continue
            command = parts[0].lower()
            name = " ".join(parts[1:]) if len(parts) > 1 else None

            if command == "exit":
                logging.info("Exit command received. Ending session.")
                break
            elif command == "help":
                console.print("Available commands: add-student <name>, remove-student <name>, list-students, help, exit")
                logging.info("Executed help command.")
            elif command in ["add-student", "remove-student", "list-students"]:
                logging.info(f"Executing command: {command} with name: {name}")
                handle_command(command, name)
            else:
                console.print(f"[red]Unknown command: '{command}'[/red]")
                logging.warning(f"Unknown command: '{command}'")

        except (KeyboardInterrupt, EOFError):
            logging.info("Interactive session ended by user.")
            break

    console.print("\n[bold cyan]Goodbye![/bold cyan]")
    logging.info("Interactive session finished.")

def main():
    parser = argparse.ArgumentParser(description="Classroom Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parser_add = subparsers.add_parser("add-student", help="Add a new student")
    parser_add.add_argument("name", help="Name of the student")

    subparsers.add_parser("list-students", help="List all students")

    parser_remove = subparsers.add_parser("remove-student", help="Remove a student")
    parser_remove.add_argument("name", help="Name of the student to remove")

    args = parser.parse_args()

    if args.command:
        name = getattr(args, 'name', None)
        handle_command(args.command, name)
    else:
        parser.print_help()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        interactive_mode()
