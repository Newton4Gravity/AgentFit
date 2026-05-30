from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pathlib import Path

from agentfit.schemas import (
    UserProfile,
    DeviceProfile,
    CalibrationRequest,
    CalibrationResponse,
    FeedbackEvent,
    ProfilePack,
)
from agentfit.calibration_engine import CalibrationEngine
from agentfit.markdown_export import export_profile_card
from agentfit.database import (
    init_db,
    upsert_user_profile,
    get_user_profile,
    upsert_device_profile,
    get_device_profile,
    list_user_devices,
    save_calibration_event,
    save_feedback_event,
)

app = FastAPI(
    title="AgentFit",
    description="A local-first Agent Calibration Control Center.",
    version="0.1.0",
)

engine = CalibrationEngine()

STATIC_DIR = Path(__file__).parent / "static"


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    index_path = STATIC_DIR / "index.html"
    return index_path.read_text(encoding="utf-8")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AgentFit",
        "version": "0.1.0"
    }


@app.post("/profiles", response_model=UserProfile)
def create_or_update_profile(profile: UserProfile):
    upsert_user_profile(profile.user_id, profile.model_dump(mode="json"))
    return profile


@app.get("/profiles/{user_id}", response_model=UserProfile)
def read_profile(user_id: str):
    data = get_user_profile(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return UserProfile(**data)


@app.post("/devices", response_model=DeviceProfile)
def create_or_update_device(device: DeviceProfile):
    upsert_device_profile(
        device.device_id,
        device.user_id,
        device.model_dump(mode="json")
    )
    return device


@app.get("/devices/{device_id}", response_model=DeviceProfile)
def read_device(device_id: str):
    data = get_device_profile(device_id)
    if not data:
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceProfile(**data)


@app.get("/profiles/{user_id}/devices")
def read_user_devices(user_id: str):
    return list_user_devices(user_id)


@app.post("/calibrate", response_model=CalibrationResponse)
def calibrate_agent(request: CalibrationRequest):
    response = engine.calibrate(request)

    save_calibration_event(
        user_id=request.user.user_id,
        request_data=request.model_dump(mode="json"),
        response_data=response.model_dump(mode="json"),
    )

    return response


@app.post("/feedback")
def store_feedback(feedback: FeedbackEvent):
    save_feedback_event(
        event_id=feedback.event_id,
        user_id=feedback.user_id,
        data=feedback.model_dump(mode="json"),
    )
    return {"status": "ok", "message": "Feedback saved"}


@app.get("/profiles/{user_id}/export.md", response_class=PlainTextResponse)
def export_profile_markdown(user_id: str):
    data = get_user_profile(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile = UserProfile(**data)
    return export_profile_card(profile)


@app.get("/profiles/{user_id}/export.json", response_model=ProfilePack)
def export_profile_json(user_id: str):
    data = get_user_profile(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile = UserProfile(**data)
    return ProfilePack(
        pack_name=f"{profile.user_id}-agentfit-profile-pack",
        profile=profile,
        safe_to_share=True,
        redaction_notes=[
            "Review before sharing.",
            "Do not include secrets, private file paths, or private project history."
        ],
    )
