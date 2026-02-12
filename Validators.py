from __future__ import annotations
from typing import Iterable, Optional
from models import Project, Task

ALLOWED_PRIORITIES = {"laag", "normaal", "hoog"}
ALLOWED_STATUSES = {"nieuw", "bezig", "afgerond"}

# Welke status-stappen zijn toegestaan
ALLOWED_TRANSITIONS = {
    ("nieuw", "bezig"),
    ("bezig", "afgerond"),
}


def ensure_not_empty(value: str, field_name: str) -> None:
    if value is None or value.strip() == "":
        raise ValueError(f"{field_name} mag niet leeg zijn.")


def ensure_project_name_unique(projects: Iterable[Project], new_name: str) -> None:
    for p in projects:
        if p.name.lower() == new_name.lower():
            raise ValueError("Projectnaam moet uniek zijn.")


def ensure_task_title_unique_in_project(project: Project, new_title: str) -> None:
    for t in project.tasks:
        if t.title.lower() == new_title.lower():
            raise ValueError("Taaktitel moet uniek zijn binnen het project.")


def ensure_priority_valid(priority: str) -> None:
    if priority not in ALLOWED_PRIORITIES:
        raise ValueError("Prioriteit moet: laag, normaal of hoog zijn.")


def ensure_status_valid(status: str) -> None:
    if status not in ALLOWED_STATUSES:
        raise ValueError("Status moet: nieuw, bezig of afgerond zijn.")


def ensure_transition_allowed(old_status: str, new_status: str) -> None:
    if (old_status, new_status) not in ALLOWED_TRANSITIONS:
        raise ValueError("Deze statusovergang is niet toegestaan (alleen nieuw→bezig→afgerond).")


def ensure_project_open(project: Project) -> None:
    if project.status == "gesloten":
        raise ValueError("Project is gesloten. Je mag geen nieuwe taken aanmaken.")


def ensure_all_tasks_completed(project: Project) -> None:
    if any(t.status != "afgerond" for t in project.tasks):
        raise ValueError("Project kan alleen gesloten worden als alle taken afgerond zijn.")


def ensure_task_completed(task: Task) -> None:
    if task.status != "afgerond":
        raise ValueError("Taak kan alleen verwijderd worden wanneer deze is afgerond.")


def ensure_task_not_locked(task: Task) -> None:
    if task.status == "afgerond":
        raise ValueError("Een afgeronde taak kan niet meer worden aangepast.")
