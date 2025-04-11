from datetime import datetime
from typing import Optional,List
from pydantic import BaseModel
from app.models import *

#BaseModels
class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class UserOutput(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
    

# Issue Models 
class IssueInput(BaseModel):
    title: str
    description: Optional[str] = None
    status: IssueStatus = IssueStatus.open
    priority: IssuePriority = IssuePriority.medium
    assignee: Optional[str] = None
    project_id: int 

class IssueOutput(IssueInput):
    id: int  
    created_at: datetime 

    class Config:
        from_attributes = True


# Project Models
class ProjectInput(BaseModel):
    name: str
    description: str

class ProjectOutput(ProjectInput):
    id: int
    issues:List[IssueOutput]
    
    class Config:
        from_attributes = True
