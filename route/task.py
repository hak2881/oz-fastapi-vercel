from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Task
from schemas import TaskCreateSchema, TaskUpdateSchema

task_router = APIRouter(
    prefix="/tasks",
    tags=["task"]
)

@task_router.post("/")
async def create_task(
        task : TaskCreateSchema,
        db: Session= Depends(get_db),
        user: dict = Depends(get_current_user)
):
    new_task = Task(
        title = task.title,

        user_id = user.user_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task.title

@task_router.get("/")
async def get_all_tasks(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == user.user_id).all()
    if not tasks:
        return {"msg" : "You have no task"}
    return tasks

@task_router.get("/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    task = db.query(Task).filter(Task.task_id == task_id).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="No task_id"
        )
    if task.user_id != user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You dont have authorization"
        )
    return task

@task_router.patch("/{task_id}")
async def update_task(update_task: TaskUpdateSchema, task_id: int, db: Session =Depends(get_db), user: dict = Depends(get_current_user)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="No task_id"
        )
    if task.user_id != user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You dont have Authorization"
        )
    for key, value in update_task.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)

    return task

@task_router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="No task_id"
        )
    if task.user_id != user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You dont have Authorization"
        )

    db.delete(task)
    db.commit()

    return {
        "msg": "Success delete"
    }