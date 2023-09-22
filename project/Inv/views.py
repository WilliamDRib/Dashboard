from django.shortcuts import render, redirect
from .models import Product, Order, Customer
from .forms import OrderForm

# Create your views here.

def dashboard(request):
    orders=Order.objects.all()
    total_order=orders.count()
    deliver=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    customer=Customer.objects.all()

    context={
        'orders': orders,
        'total_order': total_order,
        'deliver': deliver,
        'pending': pending,
        'customer': customer,
    }

    return render(request,'Inv/dashboard.html', context)


def product(request):
    item=Product.objects.all()

    context={
        'item':item
    }

    return render(request,'Inv/product.html', context)
 

def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test) 
    order = customer.order_set.all()
    order_count = order.count()

    context = {
        'pk_test': pk_test,
        'customer': customer,
        'order': order,
        'order_count': order_count,
    }

    return render(request,'Inv/customer.html', context)

def createOrder(request):
    form = OrderForm()

    if(request.method == "POST"):
        form = OrderForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')
    
    context = {
        'form': form,
    }

    return render(request, 'Inv/create_order.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if(request.method == "POST"):
        form = OrderForm(request.POST,instance=order)
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request,'Inv/order_create.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    
    context = {
        'order': order
    }

    return render(request, 'Inv/delete.html', context)

def statistics(request):
    customers = Customer.objects.all()
    data = [Order.objects.filter(customer=cust).count() for cust in customers]
    count = Customer.objects.all().count()

    context = {
        'customers': customers, 
        'data': data,
        'count': count,
    }

    return render(request, 'Inv/statistics.html', context)