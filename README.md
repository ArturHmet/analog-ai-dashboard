# ProHelp AI — Command Center

Real-time dashboard for the SureThing Analog platform running on Hetzner.

**Live Dashboard:** https://arturhmet.github.io/analog-ai-dashboard/

## Infrastructure
- **Orchestrator API:** http://49.12.234.219:8000/docs
- **Chat UI (Open WebUI):** http://49.12.234.219:3000
- **Workflow Engine (n8n):** http://49.12.234.219:5678
- **LLM Gateway (LiteLLM):** http://49.12.234.219:4000
- **Vector DB (Qdrant):** http://49.12.234.219:6333/dashboard
- **Web Search (SearXNG):** http://49.12.234.219:8888

## Stack
- LLMs: Kimi K2, DeepSeek V3, Qwen3 (via OpenRouter)
- Memory: Qdrant + PostgreSQL
- Automation: n8n
- Agents: CrewAI
