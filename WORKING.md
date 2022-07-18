





## System Design
### Assumption
The restaurant app currently works as a self-service restaurant, which means that the customer has to again hit another endpoint to collect meals and invoice. This is due to absense of sending responses to front-end from backend without requests in REST API. (Possible solution listed below)
### Architecture

![System Architecture](https://i.imgur.com/OPGYle1.png)
### Design thoughts
1. Need of ability to handle async orders, hence used Celery w/ RabbitMQ as message broker
2. If front-end is integrated, use of websockets can be done to give live status of food being prepared. Would also enable directly serving meals and invoice as ready without customer needing to check.


## Working
### Steps
1. Customer will be assigned a table/tables [ `/api/customer/table/assign`]
ex: Use this in request body 
`{
  "name": "Rugved",
  "phone_no": 43242,
  "number_of_people": 3
}`
2. Customer will order any number of meals [`/api/customer/order`]
ex. Use this in request body

{

      {
	      "customer_id": "INSERT UUID GENERATED",
      "meal_list": [
        "1","2"
      ]
    }

3. A celery worker will be assigned to 'cook' the meals. [A celery worker represents a chef to emulate behaviour]
4. Once the order is ready after sometime, the customer will have to collect the food with invoice ready. [`/api/customer/UUID/invoice`]

### Corner cases which are not implemented
1. Wrong table
2. Wrong order
3. Discounted food (coupons)
4. Table reservations
5. Meal not available from kitchen side.
