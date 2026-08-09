from pathlib import Path

import yaml
from pydantic import TypeAdapter

from investor.domain.models import AgentProfile

_PROFILE_ADAPTER = TypeAdapter(AgentProfile)


def load_profiles(directory: Path) -> dict[str, AgentProfile]:
    profiles: dict[str, AgentProfile] = {}
    if not directory.is_dir():
        raise FileNotFoundError(f"Agent configuration directory does not exist: {directory}")

    for path in sorted(directory.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        profile = _PROFILE_ADAPTER.validate_python(payload)
        if profile.name in profiles:
            raise ValueError(f"Duplicate agent profile '{profile.name}' in {path}.")
        profiles[profile.name] = profile

    if not profiles:
        raise ValueError(f"No agent profiles found in {directory}.")
    return profiles
