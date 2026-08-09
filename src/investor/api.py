from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from investor.config import get_settings
from investor.domain.models import ResearchReport, ResearchRequest
from investor.guardrails import GuardrailViolation
from investor.runtime import Runtime, create_runtime


def create_app(runtime: Runtime | None = None) -> FastAPI:
    active_runtime = runtime or create_runtime()
    settings = get_settings()
    app = FastAPI(
        title="Investor Research Agents",
        version="0.1.0",
        description="API for guarded, evidence-led research agents.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.web_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    def get_runtime() -> Runtime:
        return active_runtime

    RuntimeDependency = Annotated[Runtime, Depends(get_runtime)]

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    @app.get("/api/agents")
    async def agents(current: RuntimeDependency) -> dict[str, tuple[str, ...]]:
        return {"agents": current.orchestrator.agent_names()}

    @app.get("/api/skills")
    async def skills(current: RuntimeDependency) -> dict[str, tuple[str, ...]]:
        return {"skills": current.skills.names()}

    @app.post("/api/research", response_model=ResearchReport)
    async def research(
        request: ResearchRequest,
        current: RuntimeDependency,
    ) -> ResearchReport:
        try:
            return await current.orchestrator.research(request)
        except (GuardrailViolation, LookupError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    return app


app = create_app()
