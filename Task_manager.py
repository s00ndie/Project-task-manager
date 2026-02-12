from __future__ import annotations

from datetime import datetime
from typing import Optional

from models import Project, Task
from validators import (
    ensure_not_empty,
    ensure_task_title_unique,
    ensure_priority_valid,
    ensure_project_open,
    ensure_status_valid,
    ensure_transition_allowed,
    ensure_task_completed,
    ensure_task_not_locked,
)


class TaskManager:
    def find_task(self, project: Project, title: str) -> Optional[Task]:
        title = (title or "").strip()
        for t in project.tasks:
            if t.title.lower() == title.lower():
                return t
        return None

    def add_task(self, project: Project, title: str, description: str = "", priority: str = "normaal") -> Task:
        ensure_project_open(project)
        ensure_not_empty(title, "Taaktitel")
        ensure_task_title_unique(project, title)
        ensure_priority_valid(priority)

        task = Task(
            title=title.strip(),
            description=(description or "").strip(),
            priority=priority,
            status="nieuw",
            created_at=datetime.now(),
            completed_at=None,
        )
        project.tasks.append(task)
        return task

    def change_status(self, project: Project, title: str, new_status: str) -> None:
        task = self.find_task(project, title)
        if not task:
            raise ValueError("Taak niet gevonden.")

        ensure_task_not_locked(task)
        ensure_status_valid(new_status)
        ensure_transition_allowed(task.status, new_status)

        task.status = new_status
        if new_status == "afgerond":
            task.completed_at = datetime.now()

    def delete_task(self, project: Project, title: str) -> None:
        task = self.find_task(project, title)
        if not task:
            raise ValueError("Taak niet gevonden.")

        ensure_task_completed(task)
        project.tasks.remove(task)