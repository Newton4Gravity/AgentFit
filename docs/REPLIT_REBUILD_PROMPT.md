# Replit Rebuild Prompt for AgentFit

Use this prompt in Replit Agent when the generated app does not match the intended AgentFit product.

## Goal

Rebuild the app as **AgentFit**, an adaptive calibration control center for AI agents.

Do not build a generic chatbot.
Do not build a simple profile form only.
Do not build a normal task manager.

AgentFit must help a user create, export, import, and share calibration profiles that tell an AI agent how to behave for a specific user, device, task, model set, risk level, privacy level, and tool environment.

## Product definition

AgentFit answers this question before an agent acts:

> Given this user, this task, this device, this model set, and this risk level, what should the agent do next?

The output should be a structured agent configuration, not just a chat response.

## Required user flow

The app needs this main workflow:

1. User creates a personal calibration profile.
2. User adds one or more devices.
3. User enters a task they want an agent to perform.
4. App classifies the task.
5. App recommends an agent configuration.
6. App shows a clear calibration result.
7. User can export that result as Markdown or JSON.
8. User can share profile packs with friends.
9. User can import a profile pack and preview it before applying.
10. User can leave feedback after a calibration result.

## Required screens

### 1. Dashboard

Show:

- active profile
- connected or saved devices
- recent calibration results
- buttons for:
  - New Calibration
  - Create Profile
  - Add Device
  - Import Pack
  - Export Pack

### 2. Profile Builder

Fields:

- display name
- skill level: beginner, intermediate, advanced, expert
- preferred style: concise, step_by_step, detailed, examples_first
- risk tolerance: low, medium, high
- privacy preference: low, medium, high
- prefers open source
- prefers local-first
- likes Markdown
- wants full code
- project anchor mode

### 3. Device Builder

Fields:

- device name
- device type: phone, tablet, laptop, desktop, server, microcontroller
- operating system
- RAM
- GPU availability
- battery sensitive
- network quality
- can run Python
- can run Docker
- can access files

### 4. Task Intake

Fields:

- task description
- task category:
  - general
  - coding
  - research
  - writing
  - data_analysis
  - automation
  - planning
  - knowledge_base
  - hardware
  - security_lab
- complexity: simple, medium, complex
- requires tools
- requires file access
- requires web access
- requires code execution
- estimated sensitivity
- destructive potential

### 5. Calibration Result

Show a result card with:

- selected execution mode: local, cloud, hybrid
- selected model
- fallback model
- tool permissions
- autonomy level
- response verbosity
- safety notes
- agent rules
- explanation for each recommendation

Also show buttons:

- Copy as Markdown
- Copy as JSON
- Export Profile Pack
- Save Result
- Send Feedback

### 6. Profile Pack Library

The app should have sample shareable packs:

- Beginner Coding Pack
- Raspberry Pi Homelab Pack
- Obsidian Knowledge Base Pack
- Local AI Privacy Pack
- Agent Debugging Pack
- Writer Pack
- Hardware Project Pack

Each pack should have:

- name
- description
- profile settings
- behavior rules
- safe-to-share status

### 7. Import Preview

When importing a pack, do not apply it immediately.

Show:

- what settings will be changed
- what behavior rules will be added
- any privacy warning
- Apply button
- Cancel button

## Required backend logic

Implement a rule-based calibration engine.

### Execution mode rules

- If privacy preference is high, prefer local if the device can handle it.
- If task sensitivity is high, prefer local or hybrid.
- If network quality is poor, prefer local or hybrid.
- If task is complex and privacy allows it, prefer cloud or hybrid.
- If user prefers local-first, prefer local or hybrid.

### Model selection rules

Support these symbolic models for now:

- small_local_model
- fast_cloud_model
- strong_reasoning_model

Rules:

- Complex tasks prefer strong_reasoning_model.
- Coding, data analysis, hardware, security lab, and knowledge base tasks prefer strong_reasoning_model.
- High privacy plus local-first prefers small_local_model when possible.
- Battery-sensitive phone use prefers fast_cloud_model unless privacy is high.

### Tool policy rules

- File access should be blocked when risk tolerance is low unless the user confirms.
- Web access should be blocked when privacy preference is high unless the user confirms.
- Code execution should be blocked when risk tolerance is low unless the user confirms.
- Destructive actions always require confirmation.

### Agent behavior rules

- Beginner users get detailed step-by-step guidance.
- Concise users get shorter responses.
- Complex tasks get checkpoints.
- Project anchor mode adds stronger scope control and verification rules.
- Markdown preference adds Markdown output rules.
- Full-code preference adds full updated code output rules.

## Required export formats

### Markdown profile card

Export a readable `.md` card like:

```markdown
# AgentFit Profile Card

## User Style
- Skill level: beginner
- Preferred style: step_by_step
- Risk tolerance: low
- Privacy preference: high

## Agent Rules
- Ask before destructive actions.
- Verify before claiming success.
- Prefer reversible operations.
- Use step-by-step explanations.
```

### JSON profile pack

Export a machine-readable `.json` pack like:

```json
{
  "pack_name": "beginner-coding-pack",
  "version": "0.1.0",
  "safe_to_share": true,
  "profile": {
    "skill_level": "beginner",
    "preferred_style": "step_by_step",
    "risk_tolerance": "low",
    "privacy_preference": "high"
  },
  "agent_rules": [
    "Ask before destructive actions.",
    "Verify before claiming success."
  ]
}
```

## Visual design

Make the app feel like a control center, not a chatbot.

Recommended UI sections:

- left sidebar navigation
- profile summary cards
- device cards
- calibration result cards
- JSON/Markdown preview panels
- import/export buttons

Use a clean modern style.

## Acceptance criteria

The app is acceptable only if it can do all of this:

1. Create a user profile.
2. Create a device profile.
3. Run a calibration using profile + device + task.
4. Show the recommended model, execution mode, tool permissions, autonomy level, response style, and safety notes.
5. Export the result as Markdown.
6. Export the profile as JSON.
7. Import a JSON profile pack with preview-before-apply.
8. Include sample profile packs.
9. Save feedback.
10. Make it obvious that this is an agent calibration control layer, not a chatbot.

## Existing backend reference

Use the GitHub repo as the source of truth:

`Newton4Gravity/AgentFit`

The existing backend already includes:

- FastAPI app
- SQLite persistence
- schemas
- calibration engine
- Markdown export
- sample request
- tests

Preserve those ideas. Improve the frontend and workflow around them.

## Best first implementation

If Replit needs a simple stack, use:

- React frontend
- FastAPI backend
- SQLite database
- local JSON import/export

If Replit prefers a single-stack app, still keep the same product behavior and data model.

## Important warning

Do not simplify this into only a preferences form.

The important part is the calibration output:

- What model should the agent use?
- What tools should it allow?
- How autonomous should it be?
- How much explanation should it give?
- Should it use local, cloud, or hybrid execution?
- What safety rules should be active?
- What shareable profile pack can be exported?
