from django.shortcuts import render

from django.http import JsonResponse
from .models import *

import json
import datetime

from .utils import cookieCart, cartData, guestOrder
# Create your views here.


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']


    products = Product.objects.all() # get all the products from the database   
    context = {'products': products, 'cartItems': cartItems} # add the products in the context dictionary
    return render(request, 'store/store.html', context)

def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order, 'cartItems': cartItems} # pass the items and the order
    return render(request, 'store/cart.html', context)

def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)



def updateItem(request):

    data = json.loads(request.body) # get the data
    productId = data['productId'] # which was passed from the post request of fetch at the body
    action = data['action'] # same as productId

    print("Product Id: ", productId)
    print("Action: ",action)

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order= order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    # if we use forms it would be alot easier we wouldnt have to pass the data with javascript
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)  
    else:
        customer, order = guestOrder(request,data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):  # check if total matches the cart total
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse('Payment complete!', safe=False )
