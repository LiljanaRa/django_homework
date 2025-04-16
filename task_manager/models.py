from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Task category"
        verbose_name_plural = "Task categories"

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
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Task to be completed"
        verbose_name_plural = "Tasks to be completed"


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
        verbose_name = "SubTask (part of the main task)"
        verbose_name_plural = "SubTasks (parts of the main task)"

    def __str__(self):
        return self.title


