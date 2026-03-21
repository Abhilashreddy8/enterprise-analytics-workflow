from rest_framework import serializers
from .models import Task

class TaskStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['task_status']

    def validate(self, data):
        new_status = data.get('task_status')
        task = self.instance  # current task

        # Current status
        current_status = task.task_status

        # Allowed transitions
        allowed_transitions = {
            'YTS': ['WIP'],
            'WIP': ['HOLD', 'COMPLETED'],
            'HOLD': ['WIP'],
        }

        if new_status not in allowed_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f"Cannot move from {current_status} to {new_status}"
            )

        return data
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'task_id',
            'project_id',
            'project_name',
            'request_type',
            'cab_id',
            'task_status',
            'assigned_to',
            'created_by',
        ]
        read_only_fields = ['task_id', 'task_status', 'created_by']

    def create(self, validated_data):
        """
        Automatically set created_by as logged-in user (Admin)
        """
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)