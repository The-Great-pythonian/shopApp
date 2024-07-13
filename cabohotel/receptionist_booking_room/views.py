
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect    # to render layout work and redirect to another layout
from django.contrib import messages  # for feedback  messages
from django.contrib.auth import login, authenticate
from django.db.models import Sum
# Create your views here.

def builder_home(request):
    RoomsDetails_pipe = RoomsDetails.objects.all()
    sumpipe = RoomsDetails.objects.all().aggregate(Sum('price'))
    context = {'RoomsDetails_pipe': RoomsDetails_pipe,'sumpipe': sumpipe}
    return render(request, "home.html", context)

def builder_Register(request):
    if request.method == "POST":
        try:  #for handling sys error
            user1 = request.POST.get('username')
            pass1 = request.POST.get('password')
            user1 = user1.upper().strip()  #data validation to accept both upper/lower case
            #check for double registeration
            registerpipe = User.objects.filter(username=user1)
            if registerpipe.exists():
                messages.error(request, "Username is taken")
                return redirect('/Register/')  #not the leading and trailing slash to maintain same path 'regster'
            else:
                createpipe = User.objects.create(username=user1)  # pipleine type create(**kwargs) 	create a new object with given arguments
                createpipe.set_password(pass1)
                createpipe.save()
                messages.success(request, "Sucessful Account created You can login")
                return redirect('/Login/')
        except: #for handling sys error
            messages.error(request, "Something went wrong")
            return redirect('/Register/')

    return render(request, "Register.html")  # if method post else return get and  render of layout "Register.html"


def builder_Login(request):
    if request.method == "POST":
        try:
            user1 = request.POST.get('username')  # form data
            pass1 = request.POST.get('password')
            user1 = user1.upper().strip()
            login_pipe = User.objects.filter(username=user1)
            if not login_pipe.exists():
                messages.error(request, "Username not found")
                return redirect('/Login/')
            else:
                Auth_login_pipe = authenticate(username=user1, password=pass1)  #N.B username,password are feild in User table
                if Auth_login_pipe:
                    login(request, Auth_login_pipe)  ##from django.contrib.auth import login, authenticate
                    return redirect('/')
                else:
                    messages.error(request, "Wrong Password")
                    return redirect('/Login/')
        except:
            messages.error(request, "Something went wrong")
            return redirect('/Register/')

    return render(request, "Login.html")

from django.contrib.auth.decorators import login_required
@login_required(login_url="/Login/")  # prevent add cart without login first
def builder_addCart(request, X):
    userpipe = request.user  #login user
    RoomDetails_pipe = RoomsDetails.objects.get(uid=X)  # roomdetails is a subclass of Basemodel with a field UID
    shopperscart_pipe, _ = ShopperCart.objects.get_or_create(user=userpipe,payment=False)  # create values and assign to two field in shopperscart tank
    cart_items_creator = CartItems.objects.create(basket=shopperscart_pipe,room=RoomDetails_pipe)  # create values and assign to two field in cartiems tank
    messages.success(request, "items addedd Sucessfully")
    return redirect('/')


@login_required(login_url='/login/')
def builder_ShowCart(request):
    userpipe = request.user   #login user goes to the pipe
    shoppercart_pipe = ShopperCart.objects.get(user=userpipe, payment=False)
    #the unpaid logn user shopping cart goes to the pipe
    CartItems_pipe = CartItems.objects.filter(basket=shoppercart_pipe)
    #filter cartitems table (items/room, and basket cols ) using basket field (shopping cart) for the logn user

    #to prevent error in dipslaying nothing
    if CartItems_pipe:  # if pipe is not empty
    # sumpipe = CartItems.objects.filter(basket=shoppercart_pipe).aggregate(Sum('room.price'))
        context = {'CartItems_pipe': CartItems_pipe,'userpipe': userpipe}
        return render(request, "ShowCart.html", context)
    else:
        messages.error(request, "you have no items in cart, please add")
        return render(request, "ShowCart.html")
#reder the layout with the cartitems



@login_required(login_url='/login/')
def builder_RemoveCart(request, X):  # use x =id  if you want to create an indivdual specific page

    # X is the cartitems selected to be removed
    try:
        # remove items one by one based on each uid
        remove_pipe = CartItems.objects.get(uid=X)
        remove_pipe.delete()
        messages.success(request, "items  Sucessfully remove")
        return redirect('/ShowCart/')
    except:
        messages.error(request, "Something went wrong")
        return redirect('/')

@login_required(login_url='/login/')
def builder_Checkout(request):
    #get the username
    userpipe = request.user
    #pick the user shooping cart based on username
    shoppercart_pipe = ShopperCart.objects.get(user=userpipe, payment=False)
    # pick items filtered/based on  the user shooping cart
    CartItems_pipe = CartItems.objects.filter(basket=shoppercart_pipe)
    #if there are  items in  user shopping cart
    if CartItems_pipe:

        #calculate the total price of items in  userbasket...
        #this is not accurate way to get toal price  but a sample
        mylist=[]
        myitems = []
        for i in CartItems_pipe:
            price = i.room.price
            items = i.room.room_name
            mylist.append(price)
            myitems.append(items)
        totalprice_pipe = sum(mylist)  #sum the price of items in hopping basket
        myitems_pipe = str(myitems).strip('[]')  # present in readable format
        context = {'userpipe': userpipe,'CartItems_pipe': CartItems_pipe,'totalprice_pipe': totalprice_pipe,'myitems_pipe':myitems_pipe}
        return render(request, "Checkout.html", context)
    else:
        messages.error(request, "you have no items in cart, to check out")
        return redirect('/ShowCart/')

from datetime import datetime
def builder_Order(request):
    if request.method == "POST":

        try:  #for handling sys error
            user1 = request.POST.get('username')  #variable is from the form name /id
            user1 = user1.upper().strip()
            amount = request.POST.get('totalprice')
            amount = int(amount)
            deliveryfee = request.POST.get('shipping')
            deliveryfee = int(deliveryfee)
            items = request.POST.get('items')
            items = items.upper().strip()
            paymentype = request.POST.get('paymentOption')
            location = request.POST.get('address')
            location = location.upper().strip()
            # to add datetime to data sumitted by user to track time of order
            entrydate = datetime.now()  #add import datetime module,


            orderpipe = Order.objects.filter(username=user1,Totalprice=amount,ShippingFee=deliveryfee,
                                         ItemsList=items,Paymentoption=paymentype,DeliveryAddress=location )
            if orderpipe.exists():
                messages.error(request, "Your Order has already be submitted")
                return redirect('/ShowCart/')  # not the leading and trailing slash to maintain same path 'regster'
            else:
                create_pipe = Order.objects.create(username=user1, Totalprice=amount, ShippingFee=deliveryfee,
                                         ItemsList=items,Paymentoption=paymentype, DeliveryAddress=location,OrderDate= entrydate)
                create_pipe.save()  # data field is only automatically updated when calling Model.save()
                messages.success(request, "Your Order has been submitted")
                #edelete pesronal shopper cart and items  from cartitems table
                userpipe = request.user
                shoppercart_pipe = ShopperCart.objects.get(user=userpipe)
                #this filter cart for only this user
                remove_pipe = CartItems.objects.filter(basket=shoppercart_pipe)
                #this filter items for only this cart
                remove_pipe.delete()
                return redirect('/ShowCart/')
        except: #for handling sys error
            messages.error(request, "Something went wrong")
            return redirect('/ShowCart/')
    else:
        return redirect('/Checkout/')  # if method post else return get and  render of layout "Register.html"


#data nalytics reuse streamlit code
# import pandas
# def builder_analytics
# create_pipe = Order.objects.create(username=user1, Totalprice=amount,
# ShippingFee=deliveryfee,
# copy into CSV , plot grapgh, split items col for hot selling , track qty left, track pofrit
