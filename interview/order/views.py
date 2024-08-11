from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import Order, OrderTag
from .serializers import OrderSerializer, OrderTagSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class OrderListByDateRangeView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        embargo_date = self.request.query_params.get('embargo_date')

        if not start_date or not embargo_date:
            raise ValidationError("Both start_date and embargo_date are required.")

        return Order.objects.filter(
            start_date__lte=embargo_date,
            embargo_date__gte=start_date
        )