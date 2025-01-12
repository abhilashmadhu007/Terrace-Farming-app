
from django.contrib import admin
from django.urls import path
from terrace_farming_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('login/',views.login,name='login'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('user_reg/', views.user_reg,name='user_reg'),
    path('worker_reg/', views.worker_reg,name='worker_reg'),
    path('seller_reg/', views.Seller_reg,name='seller_reg'),
    path('delevery_boy_reg/', views.Delivery_boy_reg,name='delivery'),
    path('userhome/',views.userhome,name='userhome'),
    path('workerhome/',views.workerhome,name='workerhome'),
    path('sellerhome/',views.sellerhome,name="sellerhome"),
    path('seller_add_product/',views.seller_add_product,name='seller_add_product'),
    path('update_seller_quantity',views.update_seller_quantity,name='update_seller_quantity'),
    path('seller_product_remove',views.seller_product_remove,name="seller_product_remove"),
    path('user_products_view/',views.user_products_view,name='user_products_view'),
    path('user_workers_view/',views.user_workers_view,name="user_workers_view"),
    path('admin_users_view/',views.admin_users_view,name="admin_users_view"),
    path('admin_users_view/',views.admin_users_view,name="admin_users_view"),
    path('admin_workers_view/',views.admin_workers_view,name="admin_workers_view"),
    path('user_addtocart/',views.user_addtocart,name='user_addtocart'),
    path('cart_page/',views.cart_page,name="cart_page"),
    path('cart_remove/',views.cart_remove,name='cart_remove'),
    path('user_payment',views.user_payment,name='user_payment'),
    path('user_book_worker',views.user_book_worker,name='user_book_worker'),
    path('view_worker_request',views.view_worker_request,name='view_worker_request'),
    path('worker_submit_user',views.worker_submit_user,name='worker_submit_user'),
    path('assign_delivery_boy',views.assign_delivery_boy,name='assign_delivery_boy'),
    path('deliveryhome',views.delivery_home,name="delivery_home"),
    path('delivery_boy_orders',views.delivery_boy_orders,name='delivery_boy_orders'),
    path('user_bookings',views.user_bookings,name='user_bookings'),
    path('chat_with_worker/<int:booking_id>/', views.chat_with_worker, name='chat_with_worker'),
    path('approve_booking/',views.approve_booking, name='approve_booking'),
    path('chat_with_user/<int:booking_id>/', views.chat_with_user, name='chat_with_user'),
    path('approve_booking',views.approve_booking,name='approve_booking'),
    path('user_product_history',views.user_product_history,name='user_product_history')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
