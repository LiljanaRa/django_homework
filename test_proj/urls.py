"""
URL configuration for test_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from task_manager.views import (
    create_task,
    list_of_tasks,
    get_task_detail,
    task_statistics,
    SubTaskListCreateAPIView,
    SubTaskDetailUpdateDeleteAPIView
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/create/', create_task),
    path('tasks/', list_of_tasks),
    path('tasks/<int:task_id>/', get_task_detail),
    path('tasks/statistics/', task_statistics),
    path('subtasks/', SubTaskListCreateAPIView.as_view()),
    path('subtasks/<int:subtask_id>/', SubTaskDetailUpdateDeleteAPIView.as_view())
]
