import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_proj.settings')
django.setup()


from task_manager.models import Task, SubTask
from django.utils import timezone
from django.db.models import F
import datetime

# =====================================================================================
# 1. Создание записей
# =====================================================================================

# task = Task.objects.create(
#     title="Prepare presentation",
#     description="Prepare materials and slides for the presentation",
#     status="New",
#     deadline=datetime.datetime.now() + datetime.timedelta(days=3)
# )

# subtasks = [
#     SubTask(task=Task(id=4),
#             title="Gather information",
#             description="Find necessary information for the presentation",
#             status="New",
#             deadline=datetime.datetime.now() + datetime.timedelta(days=2)),
#     SubTask(task=Task(id=4),
#             title="Create slides",
#             description="Create presentation slides",
#             status="New",
#             deadline=datetime.datetime.now() + datetime.timedelta(days=1))
# ]
#
# SubTask.objects.bulk_create(subtasks)

# =====================================================================================
# 2. Чтение записей
# =====================================================================================

# all_new_tasks = Task.objects.filter(
#     status="New"
# )
#
# print(all_new_tasks)

# all_done_subtasks = SubTask.objects.filter(
#     status="Done",
#     deadline__lte=timezone.now()
# )
#
# print(all_done_subtasks)

# =====================================================================================
# 2. Изменение записей
# =====================================================================================

# Task.objects.filter(id=4).update(status="In progress")

# SubTask.objects.filter(id=7).update(deadline=F('deadline') - datetime.timedelta(days=2))

# SubTask.objects.filter(title="Create slides").update(title="Create and format presentation slides")

# =====================================================================================
# 2. Удаление записей
# =====================================================================================

# Task.objects.filter(title="Prepare presentation").delete()