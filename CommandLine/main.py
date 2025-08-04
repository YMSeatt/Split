import argparse
from classroom import Classroom
from rich.console import Console
from rich.table import Table

def main():
    console = Console()
    parser = argparse.ArgumentParser(description="Classroom Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add student command
    parser_add = subparsers.add_parser("add-student", help="Add a new student")
    parser_add.add_argument("name", help="Name of the student")

    # List students command
    subparsers.add_parser("list-students", help="List all students")

    # Remove student command
    parser_remove = subparsers.add_parser("remove-student", help="Remove a student")
    parser_remove.add_argument("name", help="Name of the student to remove")

    args = parser.parse_args()
    classroom = Classroom()

    if args.command == "add-student":
        if classroom.add_student(args.name):
            console.print(f"[green]Student '{args.name}' added.[/green]")
        else:
            console.print(f"[yellow]Student '{args.name}' already exists.[/yellow]")
    elif args.command == "list-students":
        students = classroom.list_students()
        if students:
            table = Table(title="Students")
            table.add_column("Name", style="cyan")
            for student in students:
                table.add_row(student)
            console.print(table)
        else:
            console.print("[yellow]No students in the classroom.[/yellow]")
    elif args.command == "remove-student":
        if classroom.remove_student(args.name):
            console.print(f"[green]Student '{args.name}' removed.[/green]")
        else:
            console.print(f"[red]Student '{args.name}' not found.[/red]")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
