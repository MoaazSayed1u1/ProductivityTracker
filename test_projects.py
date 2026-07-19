from services.todoist_service import get_projects

projects = get_projects()

for project in projects:
    print(project.name)