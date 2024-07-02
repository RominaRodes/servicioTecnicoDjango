from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import EmailAPIView
urlpatterns = [
    path('send-email', EmailAPIView.as_view(), name='send-email'),

]