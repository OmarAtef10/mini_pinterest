from django.urls import path
import pins.views as views

urlpatterns = [
    path('create/', views.CreatePin.as_view(), name='create_pin'),
    path('all/', views.GetAllPins.as_view(), name='get_pins'),
    path('board/<int:board_id>/', views.GetPinsByBoard.as_view(), name='get_pins_by_board'),
    path('<int:pk>/', views.GetPinById.as_view(), name='get_pin_by_id'),
]
