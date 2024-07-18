from django.urls import path
import pins.views as views

urlpatterns = [
    path('create/', views.CreatePin.as_view(), name='create_pin'),
]
