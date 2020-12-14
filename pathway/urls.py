from django.urls import path
from .views import Pathway_Detail_View


urlpatterns = [
    path('<int:pk>/', Pathway_Detail_View.as_view(), name='pathway_detail'),
    path('save-ratings/', Pathway_Detail_View.save_ratings, name='save-ratings')
]