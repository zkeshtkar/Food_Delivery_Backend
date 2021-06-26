from django.urls import path

from . import views

urlpatterns = [
    path('add/restaurant', views.RestaurantView.as_view()),
    path('update/restaurant/<int:restaurant_id>', views.RestaurantView.as_view()),
    path('add/food/<int:restaurant_id>', views.FoodView.as_view()),
    path('delete/food/<int:food_id>', views.FoodView.as_view()),
    path('update/food/<int:food_id>', views.FoodView.as_view()),
    path('get/orders/<int:restaurant_id>', views.OrderView.as_view()),
    path('update/order/<int:order_id>', views.OrderView.as_view()),
    path('restaurants', views.RestaurantView.as_view()),
    path('foods/<int:restaurant_id>', views.FoodView.as_view()),
    path('food/order/<int:order_id>', views.FoodOrder.as_view()),

]
