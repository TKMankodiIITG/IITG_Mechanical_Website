from django.urls import path
from .views import download_excel, login_view

urlpatterns = [
    path('download_excel/', download_excel, name='download_excel'),
    path('login/', login_view, name='login_view'),
    # Add other URL patterns here
]
