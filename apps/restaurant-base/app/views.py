from django.shortcuts import render
from django.http import JsonResponse
from .forms import CustomerForm, FoodForm, OrderForm, EmployeeForm
from .data_processing import Calculator
from .models import Order, Customer, Catalog, Employee,OrderItem
import json

def index(request):
    form_food = FoodForm(prefix='form_food')
    form_order = OrderForm(prefix='form_order')
    calculator = Calculator()

    if request.method == 'POST':
        form_food = FoodForm(request.POST, prefix='form_food')
        form_order = OrderForm(request.POST, prefix='form_order')
        if form_food.is_valid() and form_order.is_valid():
            form_food.save()
            form_order.save()
    else:
        form_food = FoodForm()
        form_order = OrderForm()

    context = {'form_food': form_food, 'form_order': form_order}
    return render(request, 'main.html', context)


def customer_panel(request):
    form_customer = CustomerForm(prefix='form_customer')
    if request.method == 'POST':
        form_customer = CustomerForm(request.POST, prefix='form_customer')
        if form_customer.is_valid():
            form_customer.save()
    else:
        form_customer = CustomerForm()

    context = {'form_customer': form_customer}
    return render(request, 'customer_panel.html', context=context)


def food_panel(request):
    form_food = FoodForm(prefix='form_food')
    if request.method == 'POST':
        form_food = FoodForm(request.POST, prefix='form_food')
        if form_food.is_valid():
            form_food.save()
    else:
        form_food = FoodForm()

    context = {'form_food': form_food}
    return render(request, 'food_panel.html', context=context)


def order_panel(request):
    form_order = OrderForm(prefix='form_order')
    if request.method == 'POST':
        form_order = OrderForm(request.POST, prefix='form_order')
        if form_order.is_valid():
            order = form_order.save()
            # Creating OrderItem for each item_id in the POST data
            for key, value in request.POST.items():
                if key.startswith("form_order-item_id"):
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    item_id = int(value)  # assuming the value is the id of the Catalog
                    item = Catalog.objects.get(pk=item_id)
                    OrderItem.objects.create(orderId=order, itemId=item)


    context = {'form_order': form_order}
    return render(request, 'order_panel.html', context=context)


def employee_panel(request):
    form_employee = EmployeeForm(prefix='form_employee')
    if request.method == 'POST':
        form_employee = EmployeeForm(request.POST, prefix='form_employee')
        if form_employee.is_valid():
            form_employee.save()
    else:
        form_employee = EmployeeForm()

    context = {'form_employee': form_employee}
    return render(request, 'employee_panel.html', context=context)


def order_endpoint(request):

    if request.method == 'GET':
        orders = Order.objects.all()
        orderItems = OrderItem.objects.all()
        foodItems = Catalog.objects.all()
        customers = Customer.objects.all()
        data = {
            'order': [
                {
                    'id': "O" + str(order.id),
                    'date': order.date,
                    'customer_id': "C" + str(order.customer_id),
                    'employee_id': "E" + str(order.employee_id)
                }
                for order in orders],
            'orderItems': [
                {
                    'id': "O" + str(orderItem.orderId.id),
                    'itemName': str(orderItem.itemId)
                }
                for orderItem in orderItems
            ],
            'foodItems': [
                {
                    'id': str(foodItem.id),
                    'name': str(foodItem.catalog_dish),
                    'price':  str(foodItem.catalog_price)
                }
                for foodItem in foodItems
            ],
            'customers': [
                {
                    'id':'C'+ str(customer.id),
                    'name': str(customer.customer_name)
                }
                for customer in customers
            ]
        }
        return JsonResponse(data=data)


def customer_endpoint(request):
    customers = Customer.objects.all()
    data = {
        'customer': [
            {
                'id': customer.id,
                'customer_name': customer.customer_name,
                'customer_status': customer.customer_status,
                'customer_address': customer.customer_address,
                'customer_contact': customer.customer_contact
            }
            for customer in customers
        ]
    }
    return JsonResponse(data=data)


def catalog_endpoint(request):
    catalogs = Catalog.objects.all()
    data = {
        'catalog': [
            {
                'id': catalog.id,
                'catalog_dish': catalog.catalog_dish,
                'catalog_price': catalog.catalog_price,
                'catalog_description': catalog.catalog_description
            }
            for catalog in catalogs
        ]
    }
    return JsonResponse(data=data)


def employee_endpoint(request):
    employees = Employee.objects.all()
    data = {
        'employee': [
            {
                'id': employee.id,
                'employee_name': employee.employee_name
            }
            for employee in employees
        ]
    }
    return JsonResponse(data=data)
