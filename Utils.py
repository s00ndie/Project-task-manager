from __future__ import annotations

from models import Project


def prompt(text: str) -> str:
    return input(text).strip()


def print_line() -> None:
    print("-" * 55)


def show_ok(msg: str) -> None:
    print(f"✅ {msg}")


def show_error(msg: str) -> None:
    print(f"❌ {msg}")


def print_menu() -> None:
    print_line()
    print("MENU")
    print("1) Project aanmaken")
    print("2) Projecten tonen")
    print("3) Project details tonen")
    print("4) Taak aanmaken")
    print("5) Taakstatus wijzigen")
    print("6) Project sluiten")
    print("7) Taak verwijderen")
    print("0) Stop")
    print_line()


def print_projects(projects: list[Project]) -> None:
    if not projects:
        print("Geen projecten.")
        return

    print_line()
    print("PROJECTEN")
    print_line()
    for p in projects:
        print(f"- {p.name} | status: {p.status} | taken: {len(p.tasks)}")
    print_line()


def print_project_detail(project: Project) -> None:
    print_line()
    print(f"PROJECT: {project.name} (status: {project.status})")
    if project.description:
        print(f"Omschrijving: {project.description}")
    print_line()

    if not project.tasks:
        print("Geen taken in dit project.")
        print_line()
        return

    for t in project.tasks:
        extra = ""
        if t.status == "afgerond" and t.completed_at:
            extra = f" | afgerond: {t.completed_at.strftime('%Y-%m-%d %H:%M')}"
        print(f"- {t.title} | prio: {t.priority} | status: {t.status}{extra}")
        if t.description:
            print(f"  > {t.description}")
    print_line()

    # TODO: print taken