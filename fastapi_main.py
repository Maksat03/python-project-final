from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
from database.db import session
from database.models import Project, ProjectMember, Task, User, save_obj
from database.schemas import ProjectCreateSchema, TaskCreateSchema, TaskChangeSchema, DeleteProjectSchema


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create_project/")
def create_project_view(project: ProjectCreateSchema):
    project = Project(**project.dict())
    save_obj(project)

    project_member = ProjectMember(project=project.id, user=project.admin)
    save_obj(project_member)

    return {"project": project.as_dict()}


@app.get("/get_user_projects/")
def get_user_projects_view(user_id: int):
    member_of_projects = session.query(ProjectMember).filter_by(user=user_id)
    projects = list()

    for project_member in member_of_projects:
        projects.append(session.query(Project).filter_by(id=project_member.project).first())

    return {"projects": projects}


@app.get("/get_project_tasks/")
def get_project_tasks_view(project_id: int):
    tasks = list()
    for task in session.query(Task).filter_by(project=project_id):
        project_member_username = session.query(User).filter_by(id=session.query(ProjectMember).filter_by(
            id=task.project_member).first().user).first().username
        tasks.append({"project_member_username": project_member_username,
                      **task.as_dict()})
    return {"tasks": tasks}


@app.post("/create_task/")
def create_task_view(task: TaskCreateSchema):
    user = session.query(User).filter_by(username=task.project_member_username).first()
    project_member = session.query(ProjectMember).filter_by(user=user.id).first()
    task.deadline = datetime.strptime(task.deadline, "%Y-%m-%d").date()
    task_dict = task.dict()
    del task_dict["project_member_username"]
    task_obj = Task(**task_dict, project_member=project_member.id)
    save_obj(task_obj)
    project_member_username = session.query(User).filter_by(id=session.query(ProjectMember).filter_by(
        id=task_obj.project_member).first().user).first().username
    return {"task": {"project_member_username": project_member_username, **task_obj.as_dict()}}


@app.post("/change_task_info/")
def change_task_info_view(task: TaskChangeSchema):
    user = session.query(User).filter_by(username=task.project_member_username).first()
    project_member = session.query(ProjectMember).filter_by(user=user.id).first()
    task.deadline = datetime.strptime(task.deadline, "%Y-%m-%d").date()
    task_dict = {"project_member": project_member.id, **task.dict()}
    del task_dict["project_member_username"], task_dict["id"]
    task_obj = session.query(Task).filter_by(id=task.id).first()
    for key, value in task_dict.items():
        setattr(task_obj, key, value)
    save_obj(task_obj)
    project_member_username = session.query(User).filter_by(id=session.query(ProjectMember).filter_by(
        id=task_obj.project_member).first().user).first().username
    return {"task": {"project_member_username": project_member_username, **task_obj.as_dict()}}


@app.post("/delete_task/{task_id}/")
def delete_task_view(task_id: int):
    session.query(Task).filter_by(id=task_id).delete()
    session.commit()
    return {"success": True}


@app.post("/delete_project_member_from_project/")
def delete_project_member_from_project_view(project: DeleteProjectSchema):
    session.query(ProjectMember).filter_by(project=project.project_id, user=project.user_id).delete()
    session.query(Project).filter_by(id=project.project_id, admin=project.user_id).delete()
    session.commit()
    return {"success": True}
