from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, F
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
#Vendor View
class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'vendor_id'

#PurchaseOrder View
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'purchaseorder_id'


#Performance Metrices View
@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)
    # Calculate performance metrics
    total_completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    on_time_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=models.F('order_date')).count()
    on_time_delivery_rate = (on_time_pos / total_completed_pos) * 100 if total_completed_pos > 0 else 0
    
    quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, status='completed').aggregate(avg_quality=models.Avg('quality_rating'))['avg_quality'] or 0
    
    avg_response_timedelta = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).aggregate(avg_response=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response']
    avg_response_time = avg_response_timedelta.total_seconds() if avg_response_timedelta else 0
    
    
    successful_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False).count()
    fulfillment_rate = (successful_pos / total_completed_pos) * 100 if total_completed_pos > 0 else 0
    
    # Update Vendor metrics
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = avg_response_time
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
    
    # Return metrics
    return Response({
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': avg_response_time,
        'fulfillment_rate': fulfillment_rate
    })

@csrf_exempt
@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    if request.method == 'POST':
        po = PurchaseOrder.objects.get(pk=po_id)
        po.acknowledgment_date = timezone.now()
        po.save()
        return JsonResponse({'message': 'Purchase order acknowledged successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)






