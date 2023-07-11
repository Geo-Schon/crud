from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from django.db.models import Q

from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        if search := request.GET.get('search'):
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        if products := request.GET.get('products'):
            queryset = queryset.filter(positions__product=products)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)