from django.urls import path
from .views import questions_page, questions_pack_detail_view

urlpatterns = [
    path('', questions_page, name='questions'),
    path('pack/<int:pk>', questions_pack_detail_view, name='questions_pack_detail_view'),
]