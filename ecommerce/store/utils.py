import json

from .models import *

def cookieCart(request):
    try:  # first load there is no cookie
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart: ', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping' : False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:  # if product does not exist in the database catch the error
            quant = cart[i]['quantity']
            cartItems += quant

            product = Product.objects.get(id= i)
            total = (product.price * quant)

            order['get_cart_total'] += total
            order['get_cart_items'] += quant

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': quant,
                'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems': cartItems, 'order':order, 'items' : items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)  # get the object or create it
        items = order.orderitem_set.all()  # get all the children of order
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request,data):
    print("user not logged in ...")

    print('COOKIES: ', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer, complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product, order=order, quantity=item['quantity']
        )

    return customer, order
