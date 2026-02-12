from __future__ import annotations
from typing import List, Optional
from models import Project
from validators import ensure_not_empty, ensure_project_name_unique, ensure_all_tasks_completed


class ProjectManager:
    def __init__(self) -> None:
        self._projects: List[Project] = []

    def create_project(self, name: str, description: str = "") -> Project:
        ensure_not_empty(name, "Projectnaam")
        ensure_project_name_unique(self._projects, name)
        project = Project(name=name.strip(), description=(description or "").strip())
        self._projects.append(project)
        return project

    def list_projects(self) -> List[Project]:
        return list(self._projects)

    def get_project(self, name: str) -> Optional[Project]:
        name = (name or "").strip()
        for p in self._projects:
            if p.name.lower() == name.lower():
                return p
        return None

    def close_project(self, name: str) -> None:
        project = self.get_project(name)
        if not project:
            raise ValueError("Project niet gevonden.")
        ensure_all_tasks_completed(project)
        project.status = "gesloten"
