import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from routers import dev_v1_router, test_v1_router, main_router, copy_build_router

app = FastAPI(
    title="Frontend Automation API",
    description="Pull branch and run npm run build via API",
    version="1.0.0",
)

# ── Register routers ─────────────────────────────────────────────────────────

app.include_router(dev_v1_router.router)
app.include_router(test_v1_router.router)
app.include_router(main_router.router)
app.include_router(copy_build_router.router)


# ── Health check ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def health():
    return {"status": "ok", "message": "Frontend Automation API is running"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8020, reload=False)
