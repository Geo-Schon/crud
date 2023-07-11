from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Product


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        exclude = ['id', 'stock']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        exclude = ['products']

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for position in positions:
            stock_product = StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for position in positions:
            stock_product, created = StockProduct.objects.update_or_create(stock=stock, product=position['product'])
            stock_product.quantity = position['quantity']
            stock_product.price = position['price']
            stock_product.save()
        return stock
