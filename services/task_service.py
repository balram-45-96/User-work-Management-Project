from database import tasks_collection  # ✅ Ensure this is importing correctly
from models.task import Task
from bson import ObjectId
import logging

# ✅ Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def get_tasks():
    tasks = []
    logger.info("Fetching tasks from database...")  # ✅ Log before fetching

    async for task in tasks_collection.find():
        logger.info(f"Fetched task: {task}")  # ✅ Log each task
        task_with_id = {**task, "id": str(task["_id"])}
        tasks.append(task_with_id)
        logger.info(f"Fetched task: {task_with_id}")  # ✅ Log each task
    logger.info(f"Total tasks fetched: {len(tasks)}")  # ✅ Log after fetching
    return tasks


async def create_task(task: Task):
    task_dict = task.dict()
    result = await tasks_collection.insert_one(task_dict)
    return {**task_dict, "id": str(result.inserted_id)}


async def get_task(task_id: str):
    task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    if task:
        return {**task, "id": str(task["_id"])}
    return None

async def update_task(task_id: str, task: Task):
    await tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": task.dict()})
    return {**task.dict(), "id": task_id}

async def delete_task(task_id: str):
    await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return {"message": "Task deleted successfully"}
