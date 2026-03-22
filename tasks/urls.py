from django.urls import path
from .views import CreateTaskView, UpdateTaskStatusView, ReassignTaskView, UserDashboardView, AdminDashboardView, UploadExcelView, DashboardAPIView


urlpatterns = [
    path('create/', CreateTaskView.as_view()),
    path('update-status/<int:task_id>/', UpdateTaskStatusView.as_view()),
    path('reassign/<int:task_id>/', ReassignTaskView.as_view()),
    path('dashboard/user/', UserDashboardView.as_view()),
    path('dashboard/admin/', AdminDashboardView.as_view()),
    path('upload/', UploadExcelView.as_view()),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]
