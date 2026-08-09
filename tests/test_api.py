from pathlib import Path

from fastapi.testclient import TestClient

from investor.api import create_app
from investor.config import Settings
from investor.runtime import create_runtime


def test_research_api_runs_development_provider() -> None:
    settings = Settings(
        agent_config_dir=Path("config/agents"),
        mcp_config_path=Path("config/mcp.servers.example.json"),
    )
    client = TestClient(create_app(create_runtime(settings=settings)))

    response = client.post(
        "/api/research",
        json={"query": "Assess durable competitive advantages", "agent": "research-lead"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["runs"][0]["agent"] == "research-lead"


def test_research_api_rejects_unknown_agent() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/research",
        json={"query": "A valid query", "agent": "missing"},
    )

    assert response.status_code == 400
    assert "not configured" in response.json()["detail"]
