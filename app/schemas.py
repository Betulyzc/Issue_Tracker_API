from datetime import datetime
from typing import Optional,List
from pydantic import BaseModel
from app.models import *

#BaseModels
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
        orm_mode = True


# Project Models
class ProjectInput(BaseModel):
    name: str
    description: str

class ProjectOutput(ProjectInput):
    id: int
    issues:List[IssueOutput]
    
    class Config:
        orm_mode = True
