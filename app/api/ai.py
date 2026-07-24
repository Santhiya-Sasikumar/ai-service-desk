from fastapi import APIRouter, HTTPException, status
 
from app.schemas.ticket import SummarizeRequest, SummarizeResponse
from app.services.aws_bedrock import (
    BedrockService,
    BedrockServiceError
)
 
 
router = APIRouter(prefix="/ai", tags=["AI"])
 
 
@router.post("/summarize", response_model=SummarizeResponse)
def summarize_ticket(
    payload: SummarizeRequest
) -> dict[str, str]:
    bedrock = BedrockService()
    try:
        return bedrock.summarize_ticket(payload.ticket_description)
    except BedrockServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI service is temporarily unavailable",
        ) from exc
 
 