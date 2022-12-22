from django.contrib.auth.views import LogoutView
from django.urls import path

from base.views import TaskCreateView, TaskListView, TaskUpdateView, TaskDetailView, TaskDeleteView, \
    RegisterView, CustomLoginView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('', TaskListView.as_view(), name='tasks'),
    path('task/<slug>/', TaskDetailView.as_view(), name='task'),
    path('task-update/<slug>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<slug>/', TaskDeleteView.as_view(), name='task-delete'),

    # path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]

# path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
