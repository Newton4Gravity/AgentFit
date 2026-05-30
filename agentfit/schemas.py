from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"


class PreferredStyle(str, Enum):
    concise = "concise"
    step_by_step = "step_by_step"
    detailed = "detailed"
    examples_first = "examples_first"


class RiskTolerance(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class PrivacyPreference(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class DeviceType(str, Enum):
    phone = "phone"
    tablet = "tablet"
    laptop = "laptop"
    desktop = "desktop"
    server = "server"
    microcontroller = "microcontroller"


class TaskCategory(str, Enum):
    general = "general"
    coding = "coding"
    research = "research"
    writing = "writing"
    data_analysis = "data_analysis"
    automation = "automation"
    planning = "planning"
    knowledge_base = "knowledge_base"
    hardware = "hardware"
    security_lab = "security_lab"


class TaskComplexity(str, Enum):
    simple = "simple"
    medium = "medium"
    complex = "complex"


class AutonomyLevel(str, Enum):
    explain_only = "explain_only"
    ask_before_action = "ask_before_action"
    supervised_actions = "supervised_actions"
    autonomous = "autonomous"


class ExecutionMode(str, Enum):
    local = "local"
    cloud = "cloud"
    hybrid = "hybrid"


class ResponseVerbosity(str, Enum):
    short = "short"
    medium = "medium"
    detailed = "detailed"


class UserProfile(BaseModel):
    user_id: str = Field(..., min_length=1)
    display_name: Optional[str] = None
    skill_level: SkillLevel = SkillLevel.intermediate
    preferred_style: PreferredStyle = PreferredStyle.step_by_step
    risk_tolerance: RiskTolerance = RiskTolerance.medium
    privacy_preference: PrivacyPreference = PrivacyPreference.medium
    prefers_open_source: bool = False
    prefers_local_first: bool = False
    likes_markdown: bool = True
    wants_full_code: bool = True
    project_anchor_mode: bool = False


class DeviceProfile(BaseModel):
    device_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    device_name: str = Field(..., min_length=1)
    device_type: DeviceType
    operating_system: str
    ram_gb: Optional[int] = Field(default=None, ge=1)
    has_gpu: bool = False
    battery_sensitive: bool = False
    network_quality: str = Field(
        default="good",
        description="Expected values: poor, average, good"
    )
    can_run_python: bool = False
    can_run_docker: bool = False
    can_access_files: bool = False


class TaskProfile(BaseModel):
    category: TaskCategory
    complexity: TaskComplexity
    requires_tools: bool = False
    requires_file_access: bool = False
    requires_web_access: bool = False
    requires_code_execution: bool = False
    estimated_sensitivity: PrivacyPreference = PrivacyPreference.medium
    destructive_potential: bool = False


class CalibrationRequest(BaseModel):
    user: UserProfile
    device: DeviceProfile
    task: TaskProfile
    available_models: Optional[List[str]] = Field(
        default_factory=lambda: [
            "small_local_model",
            "fast_cloud_model",
            "strong_reasoning_model"
        ]
    )


class ModelRecommendation(BaseModel):
    selected_model: str
    fallback_model: Optional[str]
    reason: str


class ToolPolicy(BaseModel):
    allow_tools: bool
    allow_file_access: bool
    allow_web_access: bool
    allow_code_execution: bool
    reason: str


class AgentBehavior(BaseModel):
    autonomy_level: AutonomyLevel
    response_verbosity: ResponseVerbosity
    should_ask_clarifying_questions: bool
    safety_notes: List[str]
    agent_rules: List[str]


class CalibrationResponse(BaseModel):
    execution_mode: ExecutionMode
    model_recommendation: ModelRecommendation
    tool_policy: ToolPolicy
    agent_behavior: AgentBehavior
    summary: str


class FeedbackEvent(BaseModel):
    event_id: str
    user_id: str
    usefulness_score: int = Field(..., ge=1, le=5)
    response_length_score: int = Field(..., ge=1, le=5)
    autonomy_score: int = Field(..., ge=1, le=5)
    speed_score: int = Field(..., ge=1, le=5)
    notes: Optional[str] = None


class ProfilePack(BaseModel):
    pack_name: str
    version: str = "0.1.0"
    profile: UserProfile
    safe_to_share: bool = True
    redaction_notes: List[str] = Field(default_factory=list)
