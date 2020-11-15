from django.urls import path

from .views import SignUpView, FORMS


urlpatterns = [

    path('signup/', SignUpView.as_view(FORMS), name='signup'),
    #path('login/', TemplateView.as_view(template_name='registration/login.html'), name='login'),
]