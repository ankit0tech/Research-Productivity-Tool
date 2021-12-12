from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('subjects/<int:pk>/', views.user_subjects, name='subjects'),
    path('profile/<int:pk>/', views.user_profile, name='profile'),
    path('update_profile/<int:pk>/', views.update_profile, name='update_profile'),
    path('delete/<int:pk>/', views.delete_profile, name='delete_profile'),
]