from django.urls import path
import pins.views as views

urlpatterns = [
    path('create/', views.CreatePin.as_view(), name='create_pin'),
    path('all/', views.GetAllPins.as_view(), name='get_pins'),
    path('board/<int:board_id>/', views.GetPinsByBoard.as_view(), name='get_pins_by_board'),
    path('<int:pk>/', views.GetPinById.as_view(), name='get_pin_by_id'),
    path('update/<int:pk>/', views.UpdatePin.as_view(), name='update_pin'),
    path('delete/<int:pk>/', views.UpdatePin.as_view(), name='delete_pin'),
    path("add-pin-image/<int:pin_id>/", views.UpdatePinImage.as_view(), name="update_pin_image"),
    path("delete-pin-image/<int:pin_id>/<int:image_id>/", views.UpdatePinImage.as_view(), name="delete_pin_image"),
    path("update-pin-image/<int:pin_id>/<int:image_id>/", views.UpdatePinImage.as_view(), name="delete_pin_image"),

]
