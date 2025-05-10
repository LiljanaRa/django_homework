from django.db.models.functions import ExtractWeekDay
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from task_manager.models import Task, SubTask
from task_manager.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    SubTaskListSerializer)
import datetime


class TaskListCreateAPIView(APIView):

    def get_queryset(self, request: Request):
        WEEKDAY_NAMES = {
            'sunday': 1,
            'monday': 2,
            'tuesday': 3,
            'wednesday': 4,
            'thursday': 5,
            'friday': 6,
            'saturday': 7
        }

        queryset = Task.objects.all()

        weekdays = request.query_params.get('weekday')

        if weekdays:
            weekday = weekdays.lower()
            weekday_num = WEEKDAY_NAMES.get(weekday)
            queryset = queryset.annotate(
            weekday=ExtractWeekDay('deadline')
        ).filter(weekday=weekday_num)

        return queryset

    def get(self, request: Request):
        tasks = self.get_queryset(request=request)
        serializer = TaskListSerializer(tasks, many=True)

        return Response(serializer.data)

    def post(self, request: Request):
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailUpdateDeleteAPIView(APIView):

    def get(self, request: Request, **kwargs):
        try:
            task = Task.objects.get(id=kwargs['task_id'])
        except Task.DoesNotExist:
            return Response(
                data={
                    "message": "Task not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskListSerializer(task)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, **kwargs):
        try:
            task = Task.objects.get(id=kwargs['task_id'])
        except Task.DoesNotExist:
            return Response(
                data={
                    "message": "Task not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskListSerializer(instance=task, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request: Request, **kwargs):
        try:
            task = Task.objects.get(id=kwargs['task_id'])
        except Task.DoesNotExist:
            return Response(
                data={
                    "massage": "Task not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        task.delete()

        return Response(
            data={
                "message": "Task was deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
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


class SubTaskListCreateAPIView(APIView, PageNumberPagination):
    page_size = 5

    def get_queryset(self, request: Request):
        queryset = SubTask.objects.all()

        task_title = request.query_params.get('title')
        status = request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)

        if status:
            queryset = queryset.filter(status=status)

        queryset = queryset.order_by('-created_at')

        return queryset

    def get_page_size(self, request: Request):
        page_size = request.query_params.get('page_size')

        if page_size and page_size.isdigit():
            return int(page_size)

        return self.page_size

    def get(self,request: Request):
        queryset = self.get_queryset(request=request)
        result = self.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = SubTaskListSerializer(result, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = SubTaskListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteAPIView(APIView):

    def get(self, request: Request, **kwargs):
        try:
            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "message": "Subtask not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SubTaskListSerializer(subtask)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, **kwargs):
        try:
            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "message": "Subtask not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskListSerializer(instance=subtask, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request: Request, **kwargs):
        try:
            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "massage": "Subtask not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        subtask.delete()

        return Response(
            data={
                "message": "Subtask was deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


