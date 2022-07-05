from django.urls import path
from .views import post_data,get_account,get_destination

urlpatterns=[
    path('post_data',post_data),
    path('get_account/',get_account),
    path('get_destination/',get_destination)
]