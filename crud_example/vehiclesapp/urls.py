from django.urls import path
from .views import home_view, create_view, list_view, update_view, delete_view

urlpatterns = [
    path('create/', create_view, name='create'),
    path('', list_view, name='read'),
    path('update/<int:id>/', update_view, name='update'),
    path('delete/<int:id>/', delete_view, name='delete'),
]
