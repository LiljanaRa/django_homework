from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from task_manager.models import Task, SubTask,Category


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'deadline'
        ]

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline's date cannot be in the past")

        return value


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'status',
            'deadline',
            'created_at'
        ]


class SubTaskListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    task = serializers.StringRelatedField()

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    task = SubTaskListSerializer()

    class Meta:
        model = Task
        fields = "__all__"


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = "__all__"


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        name = validated_data.get('name')

        if Category.objects.filter(name=name).exists():
            raise ValidationError({"name": "Category with this name already exists."})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        new_name = validated_data.get('name', instance.name)

        if Category.objects.filter(name=new_name).exists():
            raise ValidationError({"name": "Category with this name already exists."})

        instance.name = new_name
        instance.save()

        return instance

