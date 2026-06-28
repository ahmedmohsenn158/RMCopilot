# RMCopilot

## Project Structure

This repository is scaffolded for a full-stack `finaira-rm-copilot` setup with:

- `frontend/` for UI and experience development
- `backend/` for API, orchestration, infrastructure, and mock integrations
- `data/` for seed events and knowledge-base assets
- `.github/` for CI/CD workflows

## Groq setup

Create `RMCopilot/.env` from `.env.example`, set `GROQ_API_KEY` to a valid Groq key, and restart the backend after changing it.

If the API logs say the key was rejected, generate a new key in the Groq console and replace the old value. The backend falls back to demo responses when Groq is unavailable or the key is invalid.
