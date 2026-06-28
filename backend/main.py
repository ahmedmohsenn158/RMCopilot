from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.customers import router as customers_router
from api.alerts    import router as alerts_router
from api.chat      import router as chat_router
from api.meetings  import router as meetings_router
from api.crm       import router as crm_router
from api.events    import router as events_router
from api.emails    import router as emails_router
from api.actions   import router as actions_router

app = FastAPI(title="RM Copilot API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers_router, prefix="/api/customers", tags=["customers"])
app.include_router(alerts_router,    prefix="/api/alerts",    tags=["alerts"])
app.include_router(chat_router,      prefix="/api/chat",      tags=["chat"])
app.include_router(meetings_router,  prefix="/api/meetings",  tags=["meetings"])
app.include_router(crm_router,       prefix="/api/crm",       tags=["crm"])
app.include_router(events_router,    prefix="/api/events",    tags=["events"])
app.include_router(emails_router,    prefix="/api/email",     tags=["email"])
app.include_router(actions_router,   prefix="/api/actions",   tags=["actions"])

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.0"}