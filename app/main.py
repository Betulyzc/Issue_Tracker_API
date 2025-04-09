from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import *
from typing import Union,List
from app.models import  *
from app.schemas import *

Base.metadata.create_all(bind=engine)
application = FastAPI()

#Dynamic raising error both issues and projects.
def raise_Error(id: int, value: Union[Project, Issue]):
    if value==None:
        raise HTTPException(status_code=404,detail=f"{type(value).__name__} (ID={id}) is not found.")

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#CRUDS FOR PROJECT
# Root
@application.get("/")
def read_root():
    return {"message": "Issue Tracker FastAPI is running."}


@application.get("/projects", response_model=List[ProjectOutput])
def get_projects(db: Session=Depends(get_db)):
    return db.query(Project).all()

@application.get("/projects/{project_id}", response_model=ProjectOutput)
def get_projectByID(project_id:int , db: Session=Depends(get_db)):
    project=db.query(Project).get(project_id)
    raise_Error(project_id,project)
    return project

@application.post("/projects",response_model=ProjectOutput)
def create_projects(project_data:ProjectInput,db:Session=Depends(get_db)):
    project=Project(**project_data.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@application.put("/projects/{project_id}", response_model=ProjectOutput)
def update_projects(project_data:ProjectInput,project_id:int, db:Session=Depends(get_db)):
    project=db.query(Project).get(project_id)
    raise_Error(project_id,project)
    
    for field, value in project_data.dict().items():
        setattr(project, field, value) #Update fields one by one
    
    db.commit()
    db.refresh(project)
    return project

@application.delete("/projects/{project_id}",response_model=ProjectOutput)
def delete_project(project_id:int, db:Session=Depends(get_db)):
    project=db.query(Project).get(project_id)
    raise_Error(project_id,project)
    db.delete(project)
    db.commit()
    return project
 

#CRUDS FOR ISSUES
@application.get("/issues",response_model=List[IssueOutput])
def get_issues(db: Session=Depends(get_db)):
    return db.query(Issue).all()

@application.get("/issues/{issue_id}",response_model=IssueOutput)
def get_issueByID(issue_id:int, db:Session=Depends(get_db)):
    issue=db.query(Issue).get(issue_id)
    raise_Error(issue_id,issue)
    return issue

@application.post("/issues",response_model=IssueOutput)
def create_post(issue_input:IssueInput,db:Session=Depends(get_db)):
    issue=Issue(**issue_input.dict())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue

@application.put("/issues/{issue_id}",response_model=IssueOutput)
def update_issue(issue_id:int, issue_data:IssueInput, db:Session=Depends(get_db)):
    issue=db.query(Issue).get(issue_id)
    raise_Error(issue_id,issue)

    for field,value in issue_data.dict().items():
        setattr(issue,field,value)
    
    db.commit()
    db.refresh(issue)
    return issue

@application.delete("/issues/{issue_id}",response_model=IssueOutput)
def delete_issue(issue_id:int, db:Session=Depends(get_db)):
    issue=db.query(Issue).get(issue_id)
    raise_Error(issue_id,issue)
    db.delete(issue)
    db.commit()
    return  issue 
    