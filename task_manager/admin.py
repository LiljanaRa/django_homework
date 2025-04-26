from django.contrib import admin
from django.db.models import QuerySet

from task_manager.models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ('short_title', 'status', 'deadline', 'created_at')
    search_fields = ('short_title', 'status', 'deadline', 'created_at' )
    ordering = ('status', 'deadline')

    def short_title(self, obj: Task):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        return obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'status', 'deadline', 'created_at')
    ordering = ('status', 'deadline')

    actions = ['update_status_done']

    def update_status_done(self, request, objects: QuerySet):
        for obj in objects:
            obj.status = "Done"

            obj.save()

    update_status_done.short_description = "Status done"





