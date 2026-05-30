# AgentFit

**AgentFit** is a local-first Agent Calibration Control Center.

It helps decide how an AI agent should behave for a specific:

- user
- device
- task
- model set
- risk level
- privacy preference
- tool environment

Instead of building another chatbot, AgentFit acts as the **calibration layer** before an agent works.

## What AgentFit answers

Before an agent acts, AgentFit asks:

> Given this user, this task, this device, this model set, and this risk level, what should the agent do next?

AgentFit returns a structured policy:

```json
{
  "execution_mode": "hybrid",
  "selected_model": "strong_reasoning_model",
  "autonomy": "ask_before_action",
  "verbosity": "step_by_step",
  "tools": {
    "file_access": false,
    "web_access": true,
    "code_execution": false
  }
}
```

## MVP features

This starter repo includes:

- FastAPI backend
- SQLite persistence
- User profile storage
- Device profile storage
- Rule-based calibration engine
- Feedback event storage
- Shareable profile card export
- JSON calibration pack export
- Simple browser UI
- Example request/response files

## Project structure

```text
AgentFit/
├── agentfit/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   ├── calibration_engine.py
│   ├── markdown_export.py
│   └── static/
│       └── index.html
├── docs/
│   ├── PRODUCT_VISION.md
│   └── PROFILE_PACK_SPEC.md
├── examples/
│   ├── sample_calibration_request.json
│   └── sample_profile_card.md
├── tests/
│   └── test_calibration_engine.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```bash
uvicorn agentfit.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Test calibration endpoint

```bash
curl -X POST http://127.0.0.1:8000/calibrate \
  -H "Content-Type: application/json" \
  --data @examples/sample_calibration_request.json
```

## Main API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Simple web UI |
| GET | `/health` | Health check |
| POST | `/profiles` | Create or update user profile |
| GET | `/profiles/{user_id}` | Read user profile |
| POST | `/devices` | Create or update device profile |
| GET | `/devices/{device_id}` | Read device profile |
| POST | `/calibrate` | Get agent calibration |
| POST | `/feedback` | Store feedback |
| GET | `/profiles/{user_id}/export.md` | Export shareable Markdown profile card |
| GET | `/profiles/{user_id}/export.json` | Export JSON calibration pack |

## Shareable profile cards

AgentFit supports sanitized sharing.

Private user data should stay private. Shareable profile cards should include useful behavior patterns only.

Example:

```markdown
# AgentFit Profile Card

## User Style
- Skill level: beginner
- Preferred guidance: step_by_step
- Privacy preference: high
- Risk tolerance: low

## Agent Rules
- Ask before destructive actions.
- Verify before claiming success.
- Prefer reversible changes.
- Explain commands before using them.
```

## Roadmap

### Phase 1 — Local MVP

- [x] Rule-based calibration
- [x] SQLite persistence
- [x] Profile export
- [x] Device profiles
- [x] Feedback capture
- [x] Basic web UI

### Phase 2 — Better calibration

- [ ] Scoring-based model router
- [ ] Task classifier
- [ ] Profile import
- [ ] Profile pack marketplace folder
- [ ] Local-only mode

### Phase 3 — Agent integrations

- [ ] OpenAI-compatible system prompt export
- [ ] Claude/Gemini style prompt export
- [ ] Browser extension
- [ ] Desktop app
- [ ] Mobile-friendly UI

## License

MIT
