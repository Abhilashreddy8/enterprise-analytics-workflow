from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer
from accounts.permissions import IsAdminUserRole

from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskStatusUpdateSerializer


from .models import HoldHistory

import pandas as pd
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Task

class UpdateTaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        task = get_object_or_404(Task, task_id=task_id)

        if task.assigned_to != request.user:
            return Response({"error": "Not your task"}, status=403)

        new_status = request.data.get('task_status')

        # HOLD logic
        if new_status == 'HOLD':
            reason = request.data.get('reason')

            if not reason:
                return Response({"error": "Reason required for HOLD"}, status=400)

            HoldHistory.objects.create(
                task=task,
                reason=reason,
                created_by=request.user
            )

        # Resume from HOLD
        if task.task_status == 'HOLD' and new_status == 'WIP':
            hold = task.holds.filter(hold_end__isnull=True).last()
            if hold:
                from django.utils import timezone
                hold.hold_end = timezone.now()
                hold.save()

        serializer = TaskStatusUpdateSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReassignTaskView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def patch(self, request, task_id):
        task = get_object_or_404(Task, task_id=task_id)

        new_user_id = request.data.get('assigned_to')

        if not new_user_id:
            return Response({"error": "assigned_to is required"}, status=400)

        from accounts.models import User
        new_user = get_object_or_404(User, id=new_user_id)

        old_user = task.assigned_to

        # Update task
        task.assigned_to = new_user
        task.save()

        # Save history
        AssignmentHistory.objects.create(
            task=task,
            assigned_from=old_user,
            assigned_to=new_user,
            assigned_by=request.user
        )

        return Response({"message": "Task reassigned successfully"})


from django.db.models import Count


class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        data = Task.objects.filter(assigned_to=user).values('task_status').annotate(count=Count('task_status'))

        result = {
            "YTS": 0,
            "WIP": 0,
            "HOLD": 0,
            "COMPLETED": 0
        }

        for item in data:
            result[item['task_status']] = item['count']

        return Response(result)

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get(self, request):

        data = Task.objects.values('assigned_to__email', 'task_status') \
            .annotate(count=Count('task_status'))

        return Response(data)


User = get_user_model()


class UploadExcelView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def post(self, request):

        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_excel(file)

            tasks_created = []

            for _, row in df.iterrows():

                user = User.objects.filter(id=row['assigned_to']).first()

                if not user:
                    continue  # skip invalid users

                task = Task.objects.create(
                    project_id=row['project_id'],
                    project_name=row['project_name'],
                    request_type=row['request_type'],
                    cab_id=row['cab_id'],
                    assigned_to=user,
                    created_by=request.user
                )

                tasks_created.append(task.project_id)

            return Response({
                "message": "Tasks uploaded successfully",
                "tasks": tasks_created
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)





class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status="COMPLETED").count()
        pending_tasks = Task.objects.filter(status="PENDING").count()
        held_tasks = Task.objects.filter(status="HOLD").count()

        data = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "held_tasks": held_tasks,
        }

        return Response(data)
