from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('questions/', views.QuestionView.as_view(), name='questions'),
    path('questions/create/', views.QuestionCreateView.as_view(), name='questions'),
    path('questions/update/<int:pk>', views.QuestionUpdateView.as_view(), name='questions'),
    path('questions/delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='questions'),

    ]
