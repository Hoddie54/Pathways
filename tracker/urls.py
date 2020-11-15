from django.urls import path
from .views import DashboardView

urlpatterns = [
    path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('save-firm-ordering', DashboardView.save_firm_ordering, name='save-firm-ordering'),
]