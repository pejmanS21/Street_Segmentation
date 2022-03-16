from django.urls import path
from . import views


urlpatterns = [
    path('', views.ImageView, name='upload'),
    path('image/', views.Display, name='display'),
]