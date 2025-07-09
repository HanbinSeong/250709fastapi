from typing import List, Dict, Any, Tuple
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
import logging
import httpx

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def test_external_api():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # JSONPlaceholder API 호출
            response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API 호출 실패: {str(e)}")
