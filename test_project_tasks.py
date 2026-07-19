from services.todoist_service import get_projects, get_tasks_by_project

projects = get_projects()

for project in projects:
    print(f"\n📁 {project.name}")

    tasks = get_tasks_by_project(project.id)

    for task in tasks:
        print(f"   - {task.content}")