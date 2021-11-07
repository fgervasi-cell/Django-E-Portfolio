from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view, name='list-view'),
    path('back', views.list_view, name='list-view'),
    path('delete/<int:todo_id>', views.delete, name='delete'),
    path('update/<int:todo_id>', views.update, name='update'),
    path('new', views.create_view, name='new'),
    path('create', views.create, name="create-task")
]