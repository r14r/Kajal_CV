from django.urls import path
from board import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.list_tasks, name="tasks"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("tasks/<int:pk>/toggle/", views.toggle_task, name="toggle_task"),
    path("tasks/<int:pk>/delete/", views.delete_task, name="delete_task"),
]
