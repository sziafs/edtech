from django.urls import path
from courses import views

urlpatterns = [
    path('', views.courses, name='courses'),
    #path('course<int:id>/', views.course, name='course'),
    #path('<int:id>/', views.course, name='course'),
    path('<slug>/', views.course, name='course'),
]