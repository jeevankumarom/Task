from django.urls import path
from .views import post_data,get_account,get_destination,delete_account

urlpatterns=[
    path('post_data',post_data),
    path('get_account/',get_account),
    path('get_destination/',get_destination),
    path('delete/',delete_account)
]