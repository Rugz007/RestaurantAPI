from rest_framework import serializers
from .models import Customer, OrderedMeal


class OrderSerializer(serializers.Serializer):
    customer_id = serializers.CharField(max_length=255)
    meal_list = serializers.ListField(child=serializers.CharField(max_length=255))

class ReturnSerializer(serializers.Serializer):
    customer_id = serializers.CharField(max_length=255)
    meal_list = serializers.ListField(child=serializers.CharField(max_length=255))
    reorder = serializers.BooleanField()
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedMeal
        fields = '__all__'

