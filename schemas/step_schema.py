from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Step(BaseModel):

    #Represents one conceptual instruction or action extracted from a document.


    step_id: int = Field(
        ...,
        description="Sequential identifier for the step"
    )

    statement: str = Field(
        ...,
        description="Explanation of what the step does or describes."
    )

    syntax: List[str] = Field(
        default_factory=list,
        description="Code, command, or formal syntax associated with the step"
    )

    output: List[str] = Field(
        default_factory=list,
        description="Observed or described outputs (supports multi-line outputs)"
    )

    confidence: Optional[Literal["explicit", "implicit", "example_based"]] = Field(
        default="explicit",
        description="How clearly the step is stated in the document"
    )


class DocumentExtraction(BaseModel):
    """
    Root schema for structured extraction from a document.
    """

    steps: List[Step] = Field(
        default_factory=list,
        description="List of extracted procedural steps"
    )
