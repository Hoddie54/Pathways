from django.urls import path
from .views import questions_page

urlpatterns = [
    path('', questions_page, name='questions')
]