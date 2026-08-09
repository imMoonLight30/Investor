import "./styles.css";

interface AgentList {
  agents: string[];
}

interface ResearchReport {
  query: string;
  summary: string;
  status: "completed" | "partial" | "rejected";
  runs: Array<{
    agent: string;
    summary: string;
    steps: number;
  }>;
}

function requireElement<T extends Element>(selector: string): T {
  const element = document.querySelector<T>(selector);
  if (!element) {
    throw new Error(`Research console is missing required element: ${selector}`);
  }
  return element;
}

const form = requireElement<HTMLFormElement>("#research-form");
const query = requireElement<HTMLTextAreaElement>("#query");
const agent = requireElement<HTMLSelectElement>("#agent");
const result = requireElement<HTMLElement>("#result");

async function loadAgents(): Promise<void> {
  const response = await fetch("/api/agents");
  if (!response.ok) {
    throw new Error("Could not load agent profiles.");
  }
  const payload = (await response.json()) as AgentList;
  agent.replaceChildren(
    ...payload.agents.map((name) => {
      const option = document.createElement("option");
      option.value = name;
      option.textContent = name;
      option.selected = name === "research-lead";
      return option;
    }),
  );
}

function renderReport(report: ResearchReport): void {
  const heading = document.createElement("h2");
  heading.textContent = `${report.status}: ${report.query}`;
  const summary = document.createElement("pre");
  summary.textContent = report.summary;
  result.replaceChildren(heading, summary);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector<HTMLButtonElement>("button");
  if (!button) return;

  button.disabled = true;
  button.textContent = "Researching...";
  result.textContent = "Running the bounded agent workflow...";
  try {
    const response = await fetch("/api/research", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query.value, agent: agent.value }),
    });
    const payload = (await response.json()) as ResearchReport | { detail: string };
    if (!response.ok) {
      throw new Error("detail" in payload ? payload.detail : "Research request failed.");
    }
    renderReport(payload as ResearchReport);
  } catch (error) {
    result.textContent = error instanceof Error ? error.message : "Unexpected error.";
  } finally {
    button.disabled = false;
    button.textContent = "Run research";
  }
});

loadAgents().catch((error: unknown) => {
  result.textContent = error instanceof Error ? error.message : "Could not initialize console.";
});
