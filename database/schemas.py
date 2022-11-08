from pydantic import BaseModel, Field
from database.models import TaskStatusEnum


class ProjectCreateSchema(BaseModel):
    name: str
    admin: int = Field(alias="admin_user_id")


class TaskCreateSchema(BaseModel):
    project: int = Field(alias="project_id")
    project_member_username: str
    text: str
    deadline: str
    status: TaskStatusEnum


class TaskChangeSchema(BaseModel):
    id: int = Field(alias="task_id")
    project_member_username: str
    text: str
    deadline: str
    status: TaskStatusEnum


class DeleteProjectSchema(BaseModel):
    project_id: int
    user_id: int
