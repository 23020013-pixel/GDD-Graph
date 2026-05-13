from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Union
from datetime import datetime

class Gene(BaseModel):
    id: str = Field(..., example="Gene::5243")
    name: str
    aliases: Optional[List[str]] = None
    chromosome: Optional[str] = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, v):
        if not v.startswith("Gene::"):
            raise ValueError("ID must start with Gene::")
        return v

class Disease(BaseModel):
    id: str = Field(..., example="Disease::DOID:1612")
    name: str
    synonyms: Optional[List[str]] = None
    doid: Optional[str] = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, v):
        if not v.startswith("Disease::"):
            raise ValueError("ID must start with Disease::")
        return v

class Drug(BaseModel):
    id: str = Field(..., example="Compound::DB00945")
    name: str
    inchikey: Optional[str] = None
    drugbank_id: Optional[str] = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, v):
        if not v.startswith("Compound::"):
            raise ValueError("ID must start with Compound::")
        return v

class Edge(BaseModel):
    source_id: str
    target_id: str
    relation_type: str
    sources: List[str]
    scores: dict
    aggregated_score: float
    last_updated: datetime

class BaseEntity(BaseModel):
    id: str
    name: str
    kind: str
    # Cho phép các thuộc tính bổ sung khác
    model_config = {"extra": "allow"}

class EntityResponse(BaseModel):
    entity: Union[Gene, Disease, Drug, BaseEntity]
    labels: List[str]

class PaginatedResponse(BaseModel):
    total_count: int
    items: List[dict]
    has_next: bool
    offset: int
    limit: int
