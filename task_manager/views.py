from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from task_manager.models import Task
from task_manager.serializers import TaskCreateSerializer, TaskListSerializer, TaskDetailSerializer
import datetime

@api_view(['POST'])
def create_task(request: Request):
    data = request.data

    serializer = TaskCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            data=serializer,
            status=201
        )
    else:
        return Response(
            data=serializer.errors,
            status=400
        )


@api_view(['GET'])
def list_of_tasks(request):
    tasks = Task.objects.all()

    serializer = TaskListSerializer(tasks, many=True)

    return Response(
        data=serializer.data,
        status=200
    )


@api_view(['GET'])
def get_task_detail(request, task_id: int):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            data={
                "message": "Task not found"
            },
            status=404
        )

    serializer = TaskDetailSerializer(task)

    return Response(
        data=serializer.data,
        status=200
    )


@api_view(['GET'])
def task_statistics(request):
    tasks_count = Task.objects.all().count()
    tasks_status_new = Task.objects.filter(status="New").count()
    tasks_status_in_progress = Task.objects.filter(status="In progress").count()
    tasks_status_pending = Task.objects.filter(status="Pending").count()
    tasks_status_new_blocked = Task.objects.filter(status="Blocked").count()
    tasks_status_new_done = Task.objects.filter(status="Done").count()
    tasks_overdue = Task.objects.filter(
        deadline__lte=datetime.datetime.now()).count()

    return Response(
        data={
            "Total number of tasks": tasks_count,
            "Tasks with status New": tasks_status_new,
            "Tasks with status In progress": tasks_status_in_progress,
            "Tasks with status Pending": tasks_status_pending,
            "Tasks with status Blocked": tasks_status_new_blocked,
            "Tasks with status Done": tasks_status_new_done,
            "Number of overdue tasks": tasks_overdue
        },
        status=200
    )