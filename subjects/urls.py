from django.urls import path
from subjects import views

app_name = 'subjects'

urlpatterns = [
    path('create/', views.CreateSubject.as_view(), name='create'),
    path('update/<int:pk>/', views.UpdateSubject.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteSubject.as_view(), name='delete'),
    path('list/', views.SubjectList.as_view(), name='list'),
    path('details/<int:pk>/', views.subject_detail, name='details'),
    # urls for comment
    path('<int:pk>/create-comment/', views.CreateComment.as_view(), name='create_comment'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
]