from pydantic import BaseModel,EmailStr,Field

class LeadCreate(BaseModel):
    name : str = Field(...,min_lenght=2,max_length=25)
    email : EmailStr
    phone: str = Field(...,min_length=10,max_length=15)
    source:str