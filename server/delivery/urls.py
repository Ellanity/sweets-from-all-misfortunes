from django.urls import path

from .views import *

app_name = 'delivery'
urlpatterns = [
    path('couriers', CouriersPost.as_view()),
    path('couriers/<int:courier_id>', Couriers.as_view()),
    path('orders', Orders.as_view()),
    path('orders/assign', OrdersAssign.as_view()),
    path('orders/complete', OrdersComplete.as_view())
]
