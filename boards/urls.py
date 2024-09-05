from django.urls import path, include

import boards.views as views

urlpatterns = [
    path('', views.ListCreateBoardView.as_view(), name='list_create_board'),
    path('manage/<int:pk>/', views.ManageBoardView.as_view(), name='manage_board'),


]
