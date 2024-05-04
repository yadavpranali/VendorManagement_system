
from django.urls import path
from .views import *


urlpatterns = [
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),

    path('api/purchaseorders/',PurchaseOrderListCreateAPIView.as_view(), name='purchaseorder-list-create'),
    path('api/purchaseorders/<int:purchaseorder_id>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchaseorder-retrieve-update-destroy'),

    path('api/vendors/<int:vendor_id>/performance', get_vendor_performance, name='vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge', acknowledge_purchase_order, name='acknowledge_purchase_order'),


    
]