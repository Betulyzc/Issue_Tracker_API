from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Enum,Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum #It is used to determine some values ​​as constant.


#The fixed values ​​(enum) that the status and priority fields can take are defined.
class IssueStatus(str, enum.Enum):
    open="open"
    in_progress="in_progress"
    closed="closed"

class IssuePriority(str,enum.Enum):
    low="low"
    medium="medium"
    high="high"

class Project(Base):
    __tablename__="projects"

    id = Column( Integer, primary_key=True,index=True )
    name=Column( String, nullable=False)
    description=Column(Text)

    issues=relationship("Issue", back_populates="project", cascade="all, delete")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(IssueStatus), default=IssueStatus.open)
    priority = Column(Enum(IssuePriority), default=IssuePriority.medium)
    assignee = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="issues")
