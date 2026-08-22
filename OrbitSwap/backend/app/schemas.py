from typing import Literal, Optional
from pydantic import BaseModel, Field

class SatelliteTelemetry(BaseModel):
    satellite_id: str
    name: str ="UNKNOWN"
    battery: float = Field(ge=0, le=100)
    available_cpu: float = Field(ge=0, le=100)
    communication_quality: float = Field(ge=0, le=1)
    reliability: float = Field(ge=0, le=1)
    storage: float = Field(ge=0)
    workload: float = Field(ge=0, le=100)
    visibility_window: float = Field(ge=0)
    status: str = "READY"

class TaskRequest(BaseModel):
    task_id: str
    required_cpu: float = Field(gt=0, le=100)
    expected_duration: float = Field(gt=0)
    priority: int = Field(ge=1, le=10)
    deadline: float = Field(gt=0)
    data_size: float = Field(ge=0)
    storage_requirement: float = Field(ge=0)
    mode: Literal["hybrid","rule","ml"] = "hybrid"

class DecisionResponse(BaseModel):
    decision_id: str
    selected_satellite: Optional[str] = None
    selected_name: Optional[str] = None
    mode: str
    predicted_goodness: float = 0.0
    rule_score: float = 0.0
    confidence: float = 0.0
    rejected_candidates: list[RejectedCandidate] = []
    explanation: str
    
