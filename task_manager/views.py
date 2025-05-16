from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
    )
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAdminUser

from task_manager.models import Task, SubTask, Category
from task_manager.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    SubTaskListSerializer,
    SubTaskCreateSerializer,
    CategoryCreateSerializer)
import datetime


class TaskListCreateView(ListCreateAPIView):

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
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

        weekdays = self.request.query_params.get('weekday')

        if weekdays:
            weekday = weekdays.lower()
            weekday_num = WEEKDAY_NAMES.get(weekday)
            queryset = queryset.annotate(
            weekday=ExtractWeekDay('deadline')
        ).filter(weekday=weekday_num)

        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TaskListSerializer
        return TaskCreateSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TaskListSerializer
        return TaskCreateSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class SubTaskListCreateView(ListCreateAPIView):

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = SubTask.objects.all()

        task_title = self.request.query_params.get('title')
        status = self.request.query_params.get('status')

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)

        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SubTaskListSerializer
        return SubTaskCreateSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = SubTask.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SubTaskListSerializer
        return SubTaskCreateSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(
        detail=False,
        methods=['get',],
        url_path='statistic'
    )

    def count_tasks(self, request: Request):
        category_statistic = Category.objects.annotate(
            tasks_count=Count('category')
        )

        data = [
            {
                "id": cat.id,
                "name": cat.name,
                "tasks_count": cat.tasks_count
            }
            for cat in category_statistic
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


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