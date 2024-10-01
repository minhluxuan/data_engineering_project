from django.contrib import admin
from django.urls import path

from .views import ResultView

urlpatterns = [
    path('results/', ResultView.as_view(), name='results'),
]