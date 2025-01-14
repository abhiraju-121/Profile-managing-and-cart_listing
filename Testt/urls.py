from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.home_index, name='home_index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('deactivate_account/', views.deactivate_account, name='deactivate_account'),
    path('profile/', views.profile, name='profile'),
    path('product', views.product, name='product'),
    path('product/<int:pro_id>/', views.pro_details, name='pro_details'),
    path('product/<int:product_id>/purchase/', views.purchase, name='purchase'),
    path('cart/', views.cart_view, name='cart'),
    path('delete-cart-item/<int:cart_item_id>/', views.del_cart_view, name='del_cart_view'),
    path('order-history/', views.order_history, name='order_history'),
    path('delete_history/<int:order_id>/', views.delete_history, name='delete_history'),



    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
