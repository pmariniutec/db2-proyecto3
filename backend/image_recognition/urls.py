from django.urls import path

from .views import ImageRecognitionView

urlpatterns = [
    path('query/', ImageRecognitionView.as_view(), name='query')
]
