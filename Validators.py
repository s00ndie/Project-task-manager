from __future__ import annotations

from models import Project, Task

ALLOWED_PRIORITIES = {"laag", "normaal", "hoog"}
ALLOWED_STATUSES = {"nieuw", "bezig", "afgerond"}


ALLOWED_TRANSITIONS = {
    ("nieuw", "bezig"),
    ("bezig", "afgerond"),
}


def ensure_not_empty(value: str, field_name: str) -> None:
    if value is None or value.strip() == "":
        raise ValueError(f"{field_name} mag niet leeg zijn.")


def ensure_project_name_unique(projects: list[Project], name: str) -> None:
    for p in projects:
        if p.name.lower() == name.strip().lower():
            raise ValueError("Projectnaam moet uniek zijn.")


def ensure_task_title_unique(project: Project, title: str) -> None:
    for t in project.tasks:
        if t.title.lower() == title.strip().lower():
            raise ValueError("Taaktitel moet uniek zijn binnen het project.")


def ensure_priority_valid(priority: str) -> None:
    if priority not in ALLOWED_PRIORITIES:
        raise ValueError("Prioriteit moet: laag, normaal of hoog zijn.")


def ensure_status_valid(status: str) -> None:
    if status not in ALLOWED_STATUSES:
        raise ValueError("Status moet: nieuw, bezig of afgerond zijn.")


def ensure_transition_allowed(old_status: str, new_status: str) -> None:
    if (old_status, new_status) not in ALLOWED_TRANSITIONS:
        raise ValueError("Statusovergang niet toegestaan. Alleen nieuw→bezig→afgerond.")


def ensure_project_open(project: Project) -> None:
    if project.status == "gesloten":
        raise ValueError("Project is gesloten. Je mag geen nieuwe taken toevoegen.")


def ensure_all_tasks_completed(project: Project) -> None:
    if any(t.status != "afgerond" for t in project.tasks):
        raise ValueError("Project sluiten kan alleen als alle taken afgerond zijn.")


def ensure_task_completed(task: Task) -> None:
    if task.status != "afgerond":
        raise ValueError("Taak verwijderen kan alleen als de taak afgerond is.")


def ensure_task_not_locked(task: Task) -> None:
    if task.status == "afgerond":
        raise ValueError("Afgeronde taak mag niet meer worden aangepast.")
