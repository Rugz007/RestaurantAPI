from celery import shared_task
from .models import *
import time

@shared_task
def process_order(**kwargs):
    try:
        customer = Customer.objects.get(id=kwargs.get('customer_id'))
    except Customer.DoesNotExist:
        print("Customer not found")
        return
    if customer:
        meal_list = kwargs.get('meal_list')
        time_to_prepare = 0
        meals_in_progress = []
        for meal in meal_list:
            obj = OrderedMeal.objects.create(fk_customer=customer,fk_meal=Meal.objects.get(id=meal))
            obj.save()
            meals_in_progress.append(obj)
            time_to_prepare += obj.fk_meal.time_to_prepare
        print("Waiting for {} seconds".format(time_to_prepare))
        time.sleep(time_to_prepare)
        print("Meals ready")
        for meal in meals_in_progress:
            meal.is_ready = True
            meal.save()
        