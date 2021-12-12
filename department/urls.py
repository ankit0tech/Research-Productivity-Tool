from django.urls import path
from department import views

app_name = 'department'

urlpatterns = [
    path('list/', views.dept_list, name='list'),
    path('details/<int:pk>/', views.dept_details, name='details'),
    path('subjects/<int:pk>/', views.dept_subjects, name='subjects'),
    path('students/<int:pk>/', views.dept_students, name='students'),
]