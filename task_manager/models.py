from django.db import models
from django.db.models import UniqueConstraint


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_category_name')]

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("In progress", "In progress"),
        ("Pending", "Pending"),
        ("Blocked", "Blocked"),
        ("Done", "Done"),

    ]
    title = models.CharField(max_length=75, unique_for_date='deadline')
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_task'
        ordering = ('-created_at',)
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_task_title')]

    def __str__(self):
        return self.title


class SubTask(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("In progress", "In progress"),
        ("Pending", "Pending"),
        ("Blocked", "Blocked"),
        ("Done", "Done"),

    ]
    title = models.CharField(max_length=75)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ('-created_at',)
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_subtask_title')]

    def __str__(self):
        return self.title


