"""Core data types and schema definitions for PathFinder AI."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set

@dataclass
class RoadmapNode:
    id: str
    title: str
    type: str  # "Course", "Project", "Practice", "Assessment"
    provider: str
    duration: str
    prereqs: List[str] = field(default_factory=list)
    why: str = ""
    skills: List[str] = field(default_factory=list)
    difficulty: str = "Beginner"  # "Beginner", "Intermediate", "Advanced"
    resource_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "provider": self.provider,
            "duration": self.duration,
            "prereqs": self.prereqs,
            "why": self.why,
            "skills": self.skills,
            "difficulty": self.difficulty,
            "resource_url": self.resource_url,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoadmapNode":
        return cls(
            id=str(data.get("id", "")),
            title=str(data.get("title", "")),
            type=str(data.get("type", "Course")),
            provider=str(data.get("provider", "Open Resource")),
            duration=str(data.get("duration", "2 weeks")),
            prereqs=list(data.get("prereqs", [])),
            why=str(data.get("why", "")),
            skills=list(data.get("skills", [])),
            difficulty=str(data.get("difficulty", "Beginner")),
            resource_url=data.get("resource_url"),
        )


@dataclass
class RoadmapPhase:
    phase: str
    nodes: List[RoadmapNode] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase,
            "nodes": [n.to_dict() for n in self.nodes],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoadmapPhase":
        nodes = [RoadmapNode.from_dict(n) for n in data.get("nodes", [])]
        return cls(
            phase=str(data.get("phase", "Phase")),
            nodes=nodes,
        )


@dataclass
class RoadmapData:
    goal: str
    role: str
    phases: List[RoadmapPhase] = field(default_factory=list)
    estimated_total_weeks: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "role": self.role,
            "phases": [p.to_dict() for p in self.phases],
            "estimated_total_weeks": self.estimated_total_weeks,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoadmapData":
        phases = [RoadmapPhase.from_dict(p) for p in data.get("phases", [])]
        return cls(
            goal=str(data.get("goal", "")),
            role=str(data.get("role", "")),
            phases=phases,
            estimated_total_weeks=data.get("estimated_total_weeks"),
        )


@dataclass
class LearnerProfile:
    target_role: str = "AI & ML Engineer"
    experience_level: str = "Intermediate"  # Beginner, Intermediate, Advanced
    weekly_hours: int = 15
    skills: List[str] = field(default_factory=lambda: ["Python", "Basic Math", "SQL"])
    completed_courses: List[str] = field(default_factory=list)
    preferred_learning_style: str = "Hands-on Projects"  # "Video Courses", "Hands-on Projects", "Reading", "Interactive"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_role": self.target_role,
            "experience_level": self.experience_level,
            "weekly_hours": self.weekly_hours,
            "skills": self.skills,
            "completed_courses": self.completed_courses,
            "preferred_learning_style": self.preferred_learning_style,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LearnerProfile":
        return cls(
            target_role=str(data.get("target_role", "AI & ML Engineer")),
            experience_level=str(data.get("experience_level", "Intermediate")),
            weekly_hours=int(data.get("weekly_hours", 15)),
            skills=list(data.get("skills", ["Python", "Basic Math", "SQL"])),
            completed_courses=list(data.get("completed_courses", [])),
            preferred_learning_style=str(data.get("preferred_learning_style", "Hands-on Projects")),
        )
