from services.todoist_service import get_tasks

tasks = get_tasks()

for task in tasks:
    print(task.content)