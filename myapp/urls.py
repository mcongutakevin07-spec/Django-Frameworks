from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_todo, name='add_todo'),
    path('update/<int:id>/', views.update_todo, name='update_todo'),
    path('delete/<int:id>/', views.delete_todo, name='delete_todo'),
    path('toggle/<int:id>/', views.toggle_complete, name='toggle_complete'),

    # API
    path('api/todos/', views.TodoListAPI.as_view(), name='api_todos'),
]
