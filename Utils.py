from __future__ import annotations

from models import Project, Task
from typing import List


def prompt(text: str) -> str:
    return input(text).strip()


def print_line() -> None:
    print("-" * 60)


def show_ok(msg: str) -> None:
    print(f"✅ {msg}")


def show_error(msg: str) -> None:
    print(f"❌ {msg}")


def print_menu() -> None:
    print_line()
    print("MENU".center(60))
    print("1) Project aanmaken")
    print("2) Projecten tonen")
    print("3) Project details tonen")
    print("4) Taak aanmaken")
    print("5) Taakstatus wijzigen")
    print("6) Project sluiten")
    print("7) Taak verwijderen")
    print("8) Statistiek per project tonen   ← NIEUW")
    print("0) Stop")
    print_line()


def print_projects(projects: List[Project]) -> None:
    if not projects:
        print("Geen projecten gevonden.")
        return

    print_line()
    print("PROJECTEN OVERZICHT")
    print_line()
    for p in projects:
        closed = " (gesloten)" if p.status == "gesloten" else ""
        print(f"• {p.name}{closed} | taken: {len(p.tasks)}")
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

    # Sorteren: nieuw → bezig → afgerond, dan hoog → normaal → laag
    sorted_tasks = sorted(
        project.tasks,
        key=lambda t: (
            {"nieuw": 0, "bezig": 1, "afgerond": 2}.get(t.status, 99),
            {"hoog": 0, "normaal": 1, "laag": 2}.get(t.priority, 99)
        )
    )

    for t in sorted_tasks:
        extra = ""
        if t.completed_at:
            extra = f" | afgerond: {t.completed_at.strftime('%Y-%m-%d %H:%M')}"
        print(f"• {t.title}")
        print(f"  status: {t.status:8} | prio: {t.priority:7}{extra}")
        if t.description:
            print(f"  > {t.description}")
        print()
    print_line()


def print_project_statistics(project: Project) -> None:
    if not project.tasks:
        print("Geen taken → geen statistiek mogelijk.")
        return

    total = len(project.tasks)
    counts = {"nieuw": 0, "bezig": 0, "afgerond": 0}

    for t in project.tasks:
        counts[t.status] += 1

    done = counts["afgerond"]
    percent_done = (done / total * 100) if total > 0 else 0

    print_line()
    print(f"STATISTIEK → {project.name}")
    print_line()
    print(f"Totaal taken       : {total:3}")
    print(f"Nieuw              : {counts['nieuw']:3}")
    print(f"Bezig              : {counts['bezig']:3}")
    print(f"Afgerond           : {done:3}")
    print(f"Percentage afgerond: {percent_done:5.1f}%")
    print_line()


def print_filtered_tasks(project: Project, status_filter: str) -> None:
    if status_filter not in {"nieuw", "bezig", "afgerond", "alle"}:
        print("Ongeldige filter. Gebruik: nieuw, bezig, afgerond, alle")
        return

    tasks = [t for t in project.tasks if status_filter == "alle" or t.status == status_filter]
    if not tasks:
        print(f"Geen taken met status '{status_filter}'.")
        return

    sorted_tasks = sorted(
        tasks,
        key=lambda t: (
            {"nieuw": 0, "bezig": 1, "afgerond": 2}.get(t.status, 99),
            {"hoog": 0, "normaal": 1, "laag": 2}.get(t.priority, 99)
        )
    )

    print_line()
    print(f"TAKEN → {project.name} | filter: {status_filter}")
    print_line()
    for t in sorted_tasks:
        extra = f" | afgerond: {t.completed_at.strftime('%Y-%m-%d %H:%M')}" if t.completed_at else ""
        print(f"• {t.title} | {t.status:8} | prio: {t.priority}{extra}")
        if t.description:
            print(f"  > {t.description}")
    print_line()


def search_tasks_across_projects(projects: list[Project], search_text: str) -> None:
    search_text = (search_text or "").strip().lower()
    if not search_text:
        print("Потрібно ввести хоч якесь слово для пошуку.")
        return

    found = False
    print_line()
    print(f"ПОШУК ЗАДАЧ: '{search_text}' (по всіх проєктах)")
    print_line()

    for project in projects:
        if project.status == "gesloten":
            continue  # пропускаємо закриті проєкти

        matching_tasks = [
            t for t in project.tasks
            if search_text in t.title.lower()
        ]

        if matching_tasks:
            found = True
            print(f"Проєкт: {project.name}")
            print("-" * 40)

            # сортуємо як у детальному перегляді проєкту
            sorted_tasks = sorted(
                matching_tasks,
                key=lambda t: (
                    {"nieuw": 0, "bezig": 1, "afgerond": 2}.get(t.status, 99),
                    {"hoog": 0, "normaal": 1, "laag": 2}.get(t.priority, 99)
                )
            )

            for t in sorted_tasks:
                extra = f" | afgerond: {t.completed_at.strftime('%Y-%m-%d %H:%M')}" if t.completed_at else ""
                print(f"• {t.title}")
                print(f"  {project.name} | {t.status:8} | prio: {t.priority}{extra}")
                if t.description:
                    print(f"  > {t.description[:80]}{'...' if len(t.description) > 80 else ''}")
                print()

            print()

    if not found:
        print("Нічого не знайдено за цим запитом.")
    print_line()