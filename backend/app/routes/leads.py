from fastapi import APIRouter,HTTPException
from app.schemas import LeadCreate

router = APIRouter()

@router.post("/leads",status_code=201)
def create_lead(lead :LeadCreate):

    #custom validation
    if not lead.phone.isdigit:
        raise HTTPException(
            status_code = 400,
            detail = "Only digits are allowed"
        )
     
    #simulate saving 
    print("New Lead:",lead.dict())

    return {
        "message":"lead created successfully",
        "data":lead
    }