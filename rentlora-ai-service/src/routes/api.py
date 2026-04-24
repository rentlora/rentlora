import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import google.generativeai as genai

router = APIRouter()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("WARNING: GEMINI_API_KEY environment variable is not set. AI Features will fail.")

class RentEstimateRequest(BaseModel):
    location: str
    property_type: str
    amenities: List[str]

class RentEstimateResponse(BaseModel):
    estimated_rent: int

@router.post("/estimate", response_model=RentEstimateResponse)
async def estimate_rent(request: RentEstimateRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key is not configured on the server.")

    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You are an expert real estate appraiser.
        Estimate a realistic monthly rent for a property with the following details:
        - Location: {request.location}
        - Type: {request.property_type}
        - Amenities: {', '.join(request.amenities) if request.amenities else 'None specified'}
        
        Provide your estimate as a single integer number representing the monthly rent in USD.
        Do not include dollar signs, commas, or any other text. Just the number.
        """
        
        response = model.generate_content(prompt)
        estimated_value = response.text.strip().replace('$', '').replace(',', '')
        
        return {"estimated_rent": int(estimated_value)}
        
    except Exception as e:
        print(f"AI Estimation Error: {e}")
        # Fallback to a mock calculation if AI fails
        raise HTTPException(status_code=500, detail="Failed to generate AI estimation.")
