from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('results/', views.results, name='results'),
    path('results/info/', views.info, name='results'),

    path('register_hotel/', views.register_hotel, name='register_hotel'),
    
]