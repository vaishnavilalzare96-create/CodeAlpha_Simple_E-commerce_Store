from django.contrib import admin
from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[path('admin/',admin.site.urls),path('',views.home,name='home'),path('products/',views.products,name='products'),path('product/<int:pk>/',views.product_detail,name='product_detail'),path('cart/',views.cart,name='cart'),path('cart/add/<int:pk>/',views.add_cart,name='add_cart'),path('cart/remove/<int:pk>/',views.remove_cart,name='remove_cart'),path('cart/update/',views.update_cart,name='update_cart'),path('wishlist/',views.wishlist,name='wishlist'),path('wishlist/toggle/<int:pk>/',views.toggle_wishlist,name='toggle_wishlist'),path('checkout/',views.checkout,name='checkout'),path('orders/',views.orders,name='orders'),path('register/',views.register,name='register'),path('login/',views.user_login,name='login'),path('logout/',views.user_logout,name='logout')]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
