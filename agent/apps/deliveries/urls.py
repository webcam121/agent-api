from django.urls import path
from .views import ListDeliveryView, DetailDeliveryView, TestDeliveryView, ListPreReceiverDeliveryView, \
    RetrieveLatestPreReceiverDeliveryView

app_name = 'deliveries'

urlpatterns = [
    path('<int:receiver_id>/', ListDeliveryView.as_view()),
    path('pre_receiver/<int:pre_receiver_id>/', ListPreReceiverDeliveryView.as_view()),
    path('pre_receiver/<int:pre_receiver_id>/latest/', RetrieveLatestPreReceiverDeliveryView.as_view()),
    path('detail/<int:pk>/', DetailDeliveryView.as_view()),
    # path('test/', TestDeliveryView.as_view())
]
