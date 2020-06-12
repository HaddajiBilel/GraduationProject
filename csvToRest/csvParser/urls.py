from django.urls import path
from .views import GetData, UpdateCreateData, GetIndicators

urlpatterns = [
    path('<slug:symbol>/', GetData.as_view()),
    path('<slug:symbol>/<int:size>/', GetData.as_view()),
    path('update/<slug:symbol>/', UpdateCreateData.as_view()),
    path('indicators/<slug:symbol>/', GetIndicators.as_view()),
    path('indicators/<slug:symbol>/<int:size>/', GetIndicators.as_view()),
]
