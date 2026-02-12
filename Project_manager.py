from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from models import Project
from validators import (
    ensure_not_empty,
    ensure_project_name_unique,
    ensure_all_tasks_completed,
)

DATA_FILE = Path("data.json")


class ProjectManager:
    def __init__(self) -> None:
        self._projects: List[Project] = []
        self.load()

    def load(self) -> None:
        if not DATA_FILE.exists():
            self._projects = []
            return

        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        self._projects = [Project.from_dict(p) for p in data.get("projects", [])]

    def save(self) -> None:
        data = {"projects": [p.to_dict() for p in self._projects]}
        DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---------- Project actions ----------
    def create_project(self, name: str, description: str = "") -> Project:
        ensure_not_empty(name, "Projectnaam")
        ensure_project_name_unique(self._projects, name)

        project = Project(
            name=name.strip(),
            description=(description or "").strip(),
            status="open",
            tasks=[],
        )
        self._projects.append(project)
        self.save()
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
        self.save()
