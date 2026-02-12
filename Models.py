from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


def _dt_to_str(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() if dt else None


def _str_to_dt(s: Optional[str]) -> Optional[datetime]:
    return datetime.fromisoformat(s) if s else None


@dataclass
class Task:
    title: str
    description: str = ""
    priority: str = "normaal"          # laag, normaal, hoog
    status: str = "nieuw"              # nieuw, bezig, afgerond
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": _dt_to_str(self.created_at),
            "completed_at": _dt_to_str(self.completed_at),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "normaal"),
            status=data.get("status", "nieuw"),
            created_at=_str_to_dt(data.get("created_at")) or datetime.now(),
            completed_at=_str_to_dt(data.get("completed_at")),
        )


@dataclass
class Project:
    name: str
    description: str = ""
    status: str = "open"               # open, gesloten
    tasks: List[Task] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Project":
        return Project(
            name=data["name"],
            description=data.get("description", ""),
            status=data.get("status", "open"),
            tasks=[Task.from_dict(t) for t in data.get("tasks", [])],
        )
