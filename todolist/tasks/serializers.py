from rest_framework import serializers
from .models import Project, Task, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        from datetime import date
        if value and value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'members', 'task_count', 'created_at']

    def get_task_count(self, obj):
        return obj.tasks.count()