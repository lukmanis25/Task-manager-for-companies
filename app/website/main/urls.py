from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-task', views.create_task, name='create_task'),
    path('update-task/<int:pk>', views.update_task, name='update-task'),
]