from agentfit.schemas import (
    CalibrationRequest,
    CalibrationResponse,
    ModelRecommendation,
    ToolPolicy,
    AgentBehavior,
    ExecutionMode,
    PrivacyPreference,
    RiskTolerance,
    TaskComplexity,
    TaskCategory,
    AutonomyLevel,
    ResponseVerbosity,
    PreferredStyle,
    SkillLevel,
)


class CalibrationEngine:
    """
    Rule-based calibration engine.

    This version is intentionally transparent and easy to debug.
    Later versions can replace or extend these rules with:
    - scoring
    - model benchmarks
    - feedback learning
    - cost optimization
    - task embeddings
    """

    def calibrate(self, request: CalibrationRequest) -> CalibrationResponse:
        execution_mode = self._choose_execution_mode(request)
        model_recommendation = self._choose_model(request, execution_mode)
        tool_policy = self._choose_tool_policy(request)
        agent_behavior = self._choose_agent_behavior(request)

        summary = (
            f"Configured agent for a {request.user.skill_level.value} user "
            f"working on a {request.task.complexity.value} "
            f"{request.task.category.value} task using "
            f"{execution_mode.value} execution."
        )

        return CalibrationResponse(
            execution_mode=execution_mode,
            model_recommendation=model_recommendation,
            tool_policy=tool_policy,
            agent_behavior=agent_behavior,
            summary=summary,
        )

    def _choose_execution_mode(self, request: CalibrationRequest) -> ExecutionMode:
        user = request.user
        device = request.device
        task = request.task

        ram = device.ram_gb or 0

        if user.prefers_local_first:
            if ram >= 8 or device.can_run_python or device.can_run_docker:
                return ExecutionMode.local
            return ExecutionMode.hybrid

        if user.privacy_preference == PrivacyPreference.high:
            if ram >= 8 or device.can_run_python or device.can_run_docker:
                return ExecutionMode.local
            return ExecutionMode.hybrid

        if task.estimated_sensitivity == PrivacyPreference.high:
            if ram >= 8 or device.can_run_python or device.can_run_docker:
                return ExecutionMode.local
            return ExecutionMode.hybrid

        if device.network_quality == "poor":
            return ExecutionMode.local if ram >= 8 else ExecutionMode.hybrid

        if task.complexity == TaskComplexity.complex:
            return ExecutionMode.cloud

        return ExecutionMode.hybrid

    def _choose_model(
        self,
        request: CalibrationRequest,
        execution_mode: ExecutionMode
    ) -> ModelRecommendation:
        models = request.available_models or []
        task = request.task
        device = request.device

        def has(model_name: str) -> bool:
            return model_name in models

        if execution_mode == ExecutionMode.local and has("small_local_model"):
            return ModelRecommendation(
                selected_model="small_local_model",
                fallback_model=None,
                reason="Local execution preferred due to privacy, device, or network constraints."
            )

        if task.complexity == TaskComplexity.complex and has("strong_reasoning_model"):
            return ModelRecommendation(
                selected_model="strong_reasoning_model",
                fallback_model="fast_cloud_model" if has("fast_cloud_model") else None,
                reason="Complex tasks benefit from stronger reasoning capability."
            )

        if task.category in {
            TaskCategory.coding,
            TaskCategory.data_analysis,
            TaskCategory.automation,
            TaskCategory.knowledge_base,
            TaskCategory.security_lab,
            TaskCategory.hardware,
        } and has("strong_reasoning_model"):
            return ModelRecommendation(
                selected_model="strong_reasoning_model",
                fallback_model="fast_cloud_model" if has("fast_cloud_model") else None,
                reason="This task category benefits from stronger reasoning and verification."
            )

        if device.battery_sensitive and has("fast_cloud_model"):
            return ModelRecommendation(
                selected_model="fast_cloud_model",
                fallback_model="small_local_model" if has("small_local_model") else None,
                reason="Cloud model reduces local battery and compute usage."
            )

        if has("fast_cloud_model"):
            return ModelRecommendation(
                selected_model="fast_cloud_model",
                fallback_model="small_local_model" if has("small_local_model") else None,
                reason="Default balanced choice for speed and quality."
            )

        if models:
            return ModelRecommendation(
                selected_model=models[0],
                fallback_model=None,
                reason="Selected the first available model because no preferred model matched."
            )

        return ModelRecommendation(
            selected_model="unspecified_model",
            fallback_model=None,
            reason="No available models were provided."
        )

    def _choose_tool_policy(self, request: CalibrationRequest) -> ToolPolicy:
        user = request.user
        task = request.task

        allow_tools = task.requires_tools

        allow_file_access = (
            task.requires_file_access
            and user.risk_tolerance != RiskTolerance.low
        )

        allow_web_access = (
            task.requires_web_access
            and user.privacy_preference != PrivacyPreference.high
        )

        allow_code_execution = (
            task.requires_code_execution
            and user.risk_tolerance in {RiskTolerance.medium, RiskTolerance.high}
        )

        blocked_reasons = []

        if task.requires_file_access and not allow_file_access:
            blocked_reasons.append(
                "file access restricted because user risk tolerance is low"
            )

        if task.requires_web_access and not allow_web_access:
            blocked_reasons.append(
                "web access restricted because privacy preference is high"
            )

        if task.requires_code_execution and not allow_code_execution:
            blocked_reasons.append(
                "code execution restricted because risk tolerance is low"
            )

        if task.destructive_potential:
            blocked_reasons.append(
                "destructive actions require explicit user confirmation"
            )

        reason = (
            "; ".join(blocked_reasons)
            if blocked_reasons
            else "Tool permissions match task requirements and user safety preferences."
        )

        return ToolPolicy(
            allow_tools=allow_tools,
            allow_file_access=allow_file_access,
            allow_web_access=allow_web_access,
            allow_code_execution=allow_code_execution,
            reason=reason,
        )

    def _choose_agent_behavior(self, request: CalibrationRequest) -> AgentBehavior:
        user = request.user
        task = request.task

        safety_notes = []
        agent_rules = [
            "Do not fabricate results, citations, file changes, or tool output.",
            "Separate verified facts from assumptions.",
            "Ask before destructive or irreversible actions.",
        ]

        if user.project_anchor_mode:
            agent_rules.extend([
                "Anchor the task before execution.",
                "Preserve scope and prevent task drift.",
                "Prefer reversible operations and verification checkpoints.",
                "Deliver durable artifacts when useful.",
            ])

        if user.risk_tolerance == RiskTolerance.low:
            autonomy = AutonomyLevel.ask_before_action
            safety_notes.append(
                "Low risk tolerance: agent should ask before making changes or using sensitive tools."
            )
        elif task.complexity == TaskComplexity.complex:
            autonomy = AutonomyLevel.supervised_actions
            safety_notes.append(
                "Complex task detected: agent should provide checkpoints."
            )
        else:
            autonomy = AutonomyLevel.supervised_actions

        if task.destructive_potential:
            autonomy = AutonomyLevel.ask_before_action
            safety_notes.append(
                "Task may modify or delete resources; require confirmation before destructive actions."
            )

        if user.skill_level == SkillLevel.beginner:
            verbosity = ResponseVerbosity.detailed
            should_ask_questions = True
            agent_rules.append("Use step-by-step explanations with practical examples.")
        elif user.preferred_style == PreferredStyle.concise:
            verbosity = ResponseVerbosity.short
            should_ask_questions = False
        elif task.complexity == TaskComplexity.complex:
            verbosity = ResponseVerbosity.detailed
            should_ask_questions = True
        else:
            verbosity = ResponseVerbosity.medium
            should_ask_questions = False

        if user.preferred_style == PreferredStyle.examples_first:
            agent_rules.append("Lead with an example before abstract explanation.")

        if user.likes_markdown:
            agent_rules.append("Prefer clean Markdown for instructions, reports, and handoffs.")

        if user.wants_full_code:
            agent_rules.append("When changing code, provide the full updated code after explanation.")

        if task.estimated_sensitivity == PrivacyPreference.high:
            safety_notes.append(
                "Sensitive task: avoid unnecessary external calls and minimize exposed data."
            )

        if task.requires_code_execution:
            safety_notes.append("Run code only in a sandboxed or controlled environment.")

        return AgentBehavior(
            autonomy_level=autonomy,
            response_verbosity=verbosity,
            should_ask_clarifying_questions=should_ask_questions,
            safety_notes=safety_notes,
            agent_rules=agent_rules,
        )
