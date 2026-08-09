from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Skill:
    name: str
    description: str
    instructions: str
    required_tools: tuple[str, ...] = ()


class SkillRegistry:
    def __init__(self, skills: Iterable[Skill] = ()) -> None:
        self._skills: dict[str, Skill] = {}
        for skill in skills:
            self.register(skill)

    def register(self, skill: Skill) -> None:
        if skill.name in self._skills:
            raise ValueError(f"Skill '{skill.name}' is already registered.")
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill:
        try:
            return self._skills[name]
        except KeyError as error:
            raise LookupError(f"Skill '{name}' is not registered.") from error

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._skills))

    def instructions_for(self, names: tuple[str, ...]) -> str:
        return "\n\n".join(self.get(name).instructions for name in names)
