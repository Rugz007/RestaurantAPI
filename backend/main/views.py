from .serializers import MealSerializer, OrderSerializer, CustomerSerializer
from rest_framework import viewsets, status as http_status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .tasks import process_order
from rest_framework.permissions import AllowAny
import math

class CustomerViewSet(viewsets.ViewSet):
    parser_classes = (FormParser, JSONParser)
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=OrderSerializer)
    def place_order(self, request):
        """
        Endpoint to place an order
        """
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = serializer.validated_data.get("customer_id")
            meal_list = serializer.validated_data.get("meal_list")
            if len(meal_list) == 0:
                return Response({"message": "No meals selected"}, status=http_status.HTTP_400_BAD_REQUEST)
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return Response({"message": "Invalid Customer Id"}, status=http_status.HTTP_404_NOT_FOUND)
            tables = Table.objects.filter(fk_customer=customer)
            if len(tables) == 0:
                return Response({"message": "Customer is not on any table"}, status=http_status.HTTP_400_BAD_REQUEST)
            process_order.apply_async(kwargs={"customer_id": customer_id, "meal_list": meal_list})
        return Response({"message": "Order Given!"}, status=http_status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CustomerSerializer)
    def assign_table(self, request):
        """
        Endpoint to assign a table to a customer
        """
        #TODO: Fix existing customer to table assignment
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            table_list = []
            if serializer.validated_data.get("number_of_people") > 4:
                tables_required = math.ceil(serializer.validated_data.get("number_of_people") / 4)
                try:
                    tables = Table.objects.filter(is_occupied=False).order_by("table_no")
                    if len(tables) < tables_required:
                        return Response({"message": "Not enough tables"}, status=http_status.HTTP_400_BAD_REQUEST)
                    tables = tables[:tables_required]
                    try:
                        customer = Customer.objects.get(phone_no=serializer.validated_data.get("phone_no"))
                    except:
                        customer = serializer.save()
                    for table in tables:
                        table.is_occupied = True
                        table.fk_customer = customer
                        table.save()
                        table_list.append(table.table_no)
                except:
                    return Response({"message": "Not enough tables available"}, status=http_status.HTTP_404_NOT_FOUND)
            else:
                try:
                    table = Table.objects.get(is_occupied=False)
                    customer = serializer.save()
                    table.is_occupied = True
                    table.fk_customer = customer
                    table.save()
                    table_list.append(table.table_no)
                except Table.DoesNotExist:
                    return Response({"message": "No table available"}, status=http_status.HTTP_404_NOT_FOUND)
            return Response({"message": "Table Assigned!",'tables':table_list}, status=http_status.HTTP_200_OK)
        return Response(
            {"message": "Invalid Data!", "error": serializer.errors}, status=http_status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema()
    def gets_meals(self, request, customer_id):
        """
        Endpoint to get all meals
        """
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"message": "Invalid Customer Id"}, status=http_status.HTTP_404_NOT_FOUND)
        orders = OrderedMeal.objects.filter(fk_customer=customer, is_ready=True, is_served=False)
        if len(orders) == 0:
            return Response({"message": "No meal available"}, status=http_status.HTTP_404_NOT_FOUND)
        else:
            for order in orders:
                order.is_served = True
                order.save()
        serialized = MealSerializer(orders, many=True)
        return Response({"message": "Meals Served!", "orders": serialized.data}, status=http_status.HTTP_200_OK)

    @swagger_auto_schema(request_body=OrderSerializer)
    def return_meal(self, request):
        """
        Endpoint to return a bad cooked meal.
        """
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = serializer.validated_data.get("customer_id")
            meal_list = serializer.validated_data.get("meal_list")
            reorder = serializer.validated_data.get("reorder")
            if len(meal_list) == 0:
                return Response({"message": "No meal to return"}, status=http_status.HTTP_400_BAD_REQUEST)
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                return Response({"message": "Invalid Customer Id"}, status=http_status.HTTP_404_NOT_FOUND)
            error_meals = []
            meal_ids = []
            for meal in meal_list:
                try:
                    ordered_meal = OrderedMeal.objects.get(fk_customer=customer, id=meal)
                    ordered_meal.is_proper = False
                    meal_ids.append(ordered_meal.fk_meal.id)
                    ordered_meal.save()
                except:
                    error_meals.append(meal)
            if reorder is True:
                if len(error_meals) > 0:
                    process_order.apply_async(customer=customer, meal_list=meal_ids)
                    return Response(
                        {"message": "Reordered meals. Few were invalid", "invalid_ids": error_meals},
                        status=http_status.HTTP_200_OK,
                    )
                else:
                    process_order.apply_async(customer=customer, meal_list=meal_ids)
                    return Response({"message": "Reorder Completed!"}, status=http_status.HTTP_200_OK)
            else:
                if len(error_meals) > 0:
                    return Response(
                        {"message": "Returned valid meals, few meals were invalid.", "invalid_ids": error_meals},
                        status=http_status.HTTP_200_OK,
                    )
                else:
                    return Response({"message": "Return Completed!"}, status=http_status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Invalid Data!", "error": serializer.error}, status=http_status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema()
    def generate_invoice(self, request, customer_id):
        """
        Endpoint to generate invoice for a customer
        """
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"message": "Invalid Customer Id"}, status=http_status.HTTP_404_NOT_FOUND)
        if OrderedMeal.objects.filter(fk_customer=customer, is_ready=True, is_served=False).count() == 0:
            ordered_meals = OrderedMeal.objects.filter(fk_customer=customer, is_proper=True)
            if len(ordered_meals) == 0:
                return Response({"message": "No meal to generate invoice"}, status=http_status.HTTP_404_NOT_FOUND)
            tables = Table.objects.filter(fk_customer=customer)
            for table in tables:
                table.is_occupied = False
                table.fk_customer = None
                table.save()
            invoice = Invoice.objects.create(fk_customer=customer)

            for meal in ordered_meals:
                invoice.total_amount += meal.fk_meal.price
            invoice.is_paid = True
            invoice.save()
            return Response(
                {"message": "Invoice Generated", "invoice_id": invoice.id, "amount": invoice.total_amount},
                status=http_status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Meals are being cooked. Invoice will be served after the meals are ready."},
                status=http_status.HTTP_200_OK,
            )