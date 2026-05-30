from agentfit.calibration_engine import CalibrationEngine
from agentfit.schemas import CalibrationRequest


def test_beginner_private_code_task_uses_safe_behavior():
    payload = {
        "user": {
            "user_id": "test_user",
            "skill_level": "beginner",
            "preferred_style": "step_by_step",
            "risk_tolerance": "low",
            "privacy_preference": "high",
            "prefers_local_first": True,
            "likes_markdown": True,
            "wants_full_code": True,
            "project_anchor_mode": True
        },
        "device": {
            "device_id": "test_device",
            "user_id": "test_user",
            "device_name": "Test Laptop",
            "device_type": "laptop",
            "operating_system": "Linux",
            "ram_gb": 16,
            "has_gpu": False,
            "battery_sensitive": False,
            "network_quality": "good",
            "can_run_python": True,
            "can_run_docker": True,
            "can_access_files": True
        },
        "task": {
            "category": "coding",
            "complexity": "medium",
            "requires_tools": True,
            "requires_file_access": True,
            "requires_web_access": False,
            "requires_code_execution": True,
            "estimated_sensitivity": "medium",
            "destructive_potential": False
        },
        "available_models": [
            "small_local_model",
            "fast_cloud_model",
            "strong_reasoning_model"
        ]
    }

    request = CalibrationRequest(**payload)
    response = CalibrationEngine().calibrate(request)

    assert response.execution_mode.value == "local"
    assert response.agent_behavior.autonomy_level.value == "ask_before_action"
    assert response.agent_behavior.response_verbosity.value == "detailed"
    assert response.tool_policy.allow_code_execution is False
