from django.shortcuts import render,redirect
from django.contrib import messages
from .models import*
from django.contrib.auth import authenticate
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Users, Product, Orders, Cart
from django.db.models import Q

# Create your views here.

def index(request):
    
    return render(request, 'index.html')

def user_reg(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['passowrd']
        phone = request.POST['phone']
        place = request.POST['place']
        space = request.POST['space']
        if LoginTbl.objects.filter(username=email).exists():
            messages.info(request,'Email already exists')
        else:
            log=LoginTbl.objects.create_user(username=email,password=password,usertype='user')
            log.save()
            user=Users(name=name,email=email,phone=phone,place=place,space=space,password=password)
            user.save()
            messages.info(request,'User Registered Successfully')
    return render(request, 'user_reg.html')

def worker_reg(request):
    if request.method == 'POST':
        name = request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        proof=request.FILES['proof']
        status='available'
        if LoginTbl.objects.filter(username=email).exists():
            messages.info(request,'Email already exists')
        else:
            log=LoginTbl.objects.create_user(username=email,password=password,usertype='worker')
            log.save()
            worker=Worker(name=name,email=email,proof=proof,status=status,phone=phone)
            worker.save()
            messages.info(request,'Worker Registered Successfully')
    return render(request, 'worker_reg.html')

def Seller_reg(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        proof=request.FILES['proof']
        if LoginTbl.objects.filter(username=email).exists():
            messages.info(request,'Email already exists')
        else:
            log=LoginTbl.objects.create_user(username=email,password=password,usertype='seller')
            log.save()
            seller=Seller(name=name,email=email,proof=proof,phone=phone)
            seller.save()
            messages.success(request,'Seller Registered Successfully')
    return render(request, 'seller_reg.html')

def Delivery_boy_reg(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        proof = request.FILES['proof']
        status = 'available'
        if LoginTbl.objects.filter(username=email).exists():
            messages.info(request,'Email already exists')
        else:    
            log=LoginTbl.objects.create_user(username=email,password=password,usertype='delivery')
            log.save()
            dlvry_boy=Delivery_Boy(name=name,email=email,phone=phone,proof=proof,status=status)
            dlvry_boy.save()
            messages.success(request,'Registered Successfully')
    return render(request, 'delevery_boy_reg.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
       
        if user is None:
            messages.error(request, 'Invalid username or password')
            
        else:
            if user.is_superuser:
                return redirect('/adminhome')
            elif user.usertype=='user':
                r=Users.objects.get(email=username)
                request.session['id']=r.id
                return redirect('/userhome')
            elif user.usertype=='worker':
                request.session['email']=username
                r=Worker.objects.get(email=username)
                request.session['id']=r.id
                return redirect('/workerhome')
            elif user.usertype=='seller':
                request.session['email']=username
                r=Seller.objects.get(email=username)
                request.session['id']=r.id
                return redirect('/sellerhome')
            elif user.usertype=='delivery':
                request.session['email']=username
                r=Delivery_Boy.objects.get(email=username)
                request.session['id']=r.id
                return redirect('/deliveryhome')
            else:
                messages.info(request,'Login details missmatch')
                
 
    return render(request, 'login.html')
def adminhome(request):

    return render(request,'adminhome.html')

def userhome(request):

    return render(request,'userhome.html')

def workerhome(request):

    return render(request,'workerhome.html')

def sellerhome(request):

    return render(request,'sellerhome.html')

def seller_add_product(request):
    id=request.session["id"]
    seller=Seller.objects.get(id=id)
    if request.method =="POST":
        pname=request.POST['name']
        price=request.POST['price']
        pquantity=request.POST['quantity']
        image=request.FILES['image']
        desc=request.POST['description']
        p=Product.objects.create(name=pname,price=price,quantity=pquantity,image=image,description=desc,seller=seller)
        p.save()
        messages.success(request,'Product added successfully')
    products=Product.objects.filter(seller=seller)
    return render(request,'seller_add_product.html',{'products':products})

def update_seller_quantity(request):
    if request.method == "POST":
        quantity=int(request.POST.get('aquantity',0))
        pid=request.POST['pid']
        p=Product.objects.get(id=pid)
        p.quantity+=quantity
        p.save()
    return redirect("/seller_add_product")

def seller_product_remove(request):
    id=request.GET['id']
    rmv=Product.objects.get(id=id)
    rmv.delete()
    return redirect("/seller_add_product")

def user_products_view(request):
    product=Product.objects.all()

    return render(request,'user_products_view.html',{'products':product})

def user_workers_view(request):
    workers=Worker.objects.all()
    return render(request,'user_workers_view.html',{'workers':workers})

def admin_workers_view(request):
    workers=Worker.objects.all()
    return render(request,'admin_workers_view.html',{'workers':workers})

def admin_users_view(request):
    users=Users.objects.all()
    return render(request,'admin_users_view.html',{'users':users})


def user_addtocart(request):
   
        uid = request.session.get('id')
        if not uid:
            messages.error(request, "User is not logged in.")
            return redirect('/login')  # Redirect to login if session is missing.

        user = get_object_or_404(Users, id=uid)
        status = "cart_stage"
        date = datetime.now()

        if request.method == "POST":
            quantity = int(request.POST.get('pquantity', 0))
            pid = request.POST.get('pid')
            if not pid:
                messages.error(request, "Product ID is missing.")
                return redirect('/products')  # Redirect to product listing page.

            pdata = get_object_or_404(Product, id=pid)
            if pdata.quantity < quantity:
                messages.error(request, 'Requested quantity is not available.')
                return render(request, 'user_product_view.html', {'product': pdata})

            # Get or create the order and cart item
            order, _ = Orders.objects.get_or_create(owner=user, status=status)
            cart_item, created = Cart.objects.get_or_create(
                order=order,
                product=pdata,
                defaults={'quantity': quantity, 'date': date}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, "Product added to cart successfully!")
            return redirect('/cart_page')

        # For GET request, handle gracefully
        return render(request, 'user_product_view.html')
  # Redirect to an error page.

def cart_page(request):
    uid = request.session.get('id')
    owner=Users.objects.get(id=uid)
    status = "cart_stage"
    all_orders=Cart.objects.filter(order__owner__id=uid,order__status=status)
    grand_total = sum(int(order.quantity) * float(order.product.price) for order in all_orders)
    return render(request,'cart_page.html',{'all_orders':all_orders,'grand_total':grand_total,'uid':uid})

def cart_remove(request):
    if request.method == 'POST':
        cart_id=request.POST['order_id']
        product=Cart.objects.get(id=cart_id)
        product.delete()
        return redirect('/cart_page')

    return render(request,'cart_page.html')

def user_payment(request):
    total=request.GET['total']
    uid=request.session.get('id')
    status="Order confirmed"
    user=Users.objects.get(id=uid)
    order=Orders.objects.get(owner__id=uid,status="cart_stage")
    ordered_items=Cart.objects.filter(order=order)
    if request.method == "POST":
        for ordered_item in ordered_items:
            pid=ordered_item.product.id
            product=Product.objects.get(id=pid)
            if product.quantity>0:
                product.quantity-=ordered_item.quantity
                product.save()
            order.status=status
            order.save()
            return redirect('cart_page')
    
    return render(request,'cus_pay.html',{'total':total,'order':order})

def user_book_worker(request):
    wid=request.GET['wid']
    uid=request.session.get('id')
    worker=Worker.objects.get(id=wid)
    user=Users.objects.get(id=uid)
    date=datetime.now()
    status="available"
    book=Booking.objects.create(worker=worker,user=user,date=date,status=status)
    book.save()
    return redirect('/user_workers_view')

def view_worker_request(request):
    wid=request.session.get('id')
    worker=Worker.objects.get(id=wid)
    booking = Booking.objects.filter(worker=worker).order_by('date')
    return render(request,'view_worker_request.html',{'booking':booking})

def worker_submit_user(request):
    wid=request.GET['wid']
    worker=Worker.objects.get(id=wid)
    booking=Booking.objects.get(worker=worker)
    return redirect(request,'/view_worker_request')

def assign_delivery_boy(request):
    # Fetching "Not Delivered" orders
    not_delivered_orders = Orders.objects.filter(status='Order confirmed')

    # Fetching all available delivery boys
    delivery_boys = Delivery_Boy.objects.filter(status='available')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        delivery_boy_id = request.POST.get('delivery_boy')
        
        # Assign delivery boy to the order
        order = get_object_or_404(Orders, id=order_id)
        delivery_boy = get_object_or_404(Delivery_Boy, id=delivery_boy_id)
        
        order.delivery_boy = delivery_boy
        order.status = 'In Transit'  # Optionally update status to In Transit
        order.save()

        # Update the delivery boy's status to "Busy"
        

        messages.success(request, f"Delivery boy {delivery_boy.name} has been assigned to order {order.id}.")
        return redirect('assign_delivery_boy')

    return render(request, 'assign_delivery_boy.html', {
        'orders': not_delivered_orders,
        'delivery_boys': delivery_boys,
    })

def delivery_home(request):
    return render(request,'deliveryhome.html')

def delivery_boy_orders(request):
    did=request.session.get('id')
    # Fetching the delivery boy using the logged-in user
    delivery_boy =Delivery_Boy.objects.get(id=did)

    # Fetch orders assigned to this delivery boy
    assigned_orders = Orders.objects.filter(delivery_boy=delivery_boy, status='In Transit')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        # Get the order and mark it as delivered
        order = get_object_or_404(Orders, id=order_id)
        if order.delivery_boy == delivery_boy:
            order.status = 'Delivered'
            order.save()

            messages.success(request, f"Order {order.id} marked as delivered.")
            return redirect('delivery_boy_orders')

    return render(request, 'delivery_boy_orders.html', {
        'assigned_orders': assigned_orders,
        'delivery_boy': delivery_boy
    })

def user_bookings(request):
    id = request.session.get('id')
    if id is None:
        # Handle case where session id is not found
        return redirect('login')  # Or any appropriate action

    user = Users.objects.get(id=id)
    bookings = Booking.objects.filter(user=user)
    
    # Debugging line to check if bookings are being fetched
    print(bookings)

    return render(request, 'user_bookings.html', {'bookings': bookings,'user':user})


def chat_with_worker(request, booking_id):
    # Ensure the worker is logged in by checking if the session has 'id'
    user_id = request.session.get('id')
    if not user_id:
        return redirect('/login')  # Redirect to login if session is missing

    # Fetch the worker details
    user = Users.objects.get(id=user_id)

    # Get the booking based on the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Fetch the user associated with the booking
    worker = Worker.objects.get(id=booking.worker.id)  # This assumes the 'user' field is related to the Users model
    print(worker.name,"888888888888888888")
    # Fetch chat messages related to the booking between the worker and the user
    messages = Chat.objects.filter(worker__id=worker.id,user=user)
    for message in messages:
        print(message)

    messages = messages.order_by('created_at')
    date=datetime.now()

       

    # Handle message submission
    if request.method == 'POST':
        message = request.POST.get('msg')
        if message:
            # Create and save a new chat message
            Chat.objects.create(
                sender='user',
                booking=booking,
                worker=worker,  # This will be the logged-in worker
                user=user,  # The receiver will be the user
                message=message,
                created_at=date
            )
            # Redirect to prevent form resubmission
            return redirect('chat_with_worker',booking_id=booking.id)

    return render(request, 'user_chat.html', {
        'messages': messages,
        'booking': booking,
        'worker': worker,
        'user': user,
    })

def chat_with_user(request, booking_id):
    date=datetime.now()
    # Ensure the expert is logged in by checking if the session has 'id'
    if 'id' not in request.session:
        messages.error(request, "You need to log in first.")
        return redirect('expert_login')  # Redirect to the login page if the session is invalid
    
    worker_id = request.session['id']
    try:
        # Fetch the expert from the session ID
        worker = Worker.objects.get(id=worker_id)

        # Fetch the booking based on the booking_id
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Get the user associated with the booking
        user = booking.user  # Directly access the user from the booking instance

        # Initialize the sender (expert) and receiver (user) email
        sender = worker.email
        receiver = user.email


        # Handle POST request to send messages
        if request.method == "POST":
            message = request.POST.get('msg')
            if message:
                Chat.objects.create(sender="worker",worker=worker, user=user, message=message,booking=booking,created_at=date)
                return redirect(f'/chat_with_user/{booking_id}')  # Redirect to refresh chat

        # Retrieve all messages between the expert and the user, ordered by date
        messages = Chat.objects.filter(worker=worker, user=user) 
        messages = messages.order_by('created_at')

        return render(request, 'worker_chat.html', {
            'messages': messages,
            'sender': sender,
            'receiver': receiver,
            'worker': worker,  # Add expert to the context (optional)
            'user': user,      # Add user to the context (optional)
            'booking': booking # Add booking to the context (optional)
        })

    except Worker.DoesNotExist:
        messages.error(request, "Expert not found.")
        return redirect('expert_login')  # Redirect if the expert is not found

    except Users.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('experthome')  # Redirect if the user is not found


def approve_booking(request):
    booking_id = request.GET.get('booking_id')
    booking = get_object_or_404(Booking, id=booking_id)
    # Logic to approve booking
    booking.status = 'Approved'  # Update the booking status or any other necessary actions
    booking.save()
    return redirect('/view_worker_request')  # Redirect back to the worker's bookings page

def user_product_history(request):
    id=request.session['id']
    user=Users.objects.get(id=id)
    delivered_order=Orders.objects.filter(status='Delivered',owner=user)
    order=Cart.objects.filter(order__owner=user,order__status='Delivered')

    return render(request,'user_product_history.html',{'delivered_order':order})




