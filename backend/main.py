from fastapi import FastAPI

app = FastAPI(title="Finaira RM Copilot API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
