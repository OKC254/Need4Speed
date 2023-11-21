from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name = 'home'),
    path('upload/', views.upload, name = 'upload'),
    #path('forms/', views.VideoFormView.as_view(), name = 'forms'),
]