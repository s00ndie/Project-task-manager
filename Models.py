from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    title: str
    description: str = ""
    priority: str = "normaal"  # laag, normaal, hoog
    status: str = "nieuw"      # nieuw, bezig, afgerond
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class Project:
    name: str
    description: str = ""
    status: str = "open"       # open, gesloten
    tasks: List[Task] = field(default_factory=list)
