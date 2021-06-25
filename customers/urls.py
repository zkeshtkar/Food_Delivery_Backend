from django.urls import path

from . import views

urlpatterns = [

    path('update/profile/', views.CustomerView.as_view()),
    path('profile/', views.CustomerView.as_view()),
    path('add/order/<str:restaurant_name>/', views.OrderView.as_view()),
    path('search/<str:search_type>/<str:name>/', views.FoodSearch.as_view()),
    path('foods/', views.FoodSearch.as_view()),
    path('orders/', views.OrderView.as_view()),
    path('food/order/<int:order_id>', views.FoodOrder.as_view()),
    path('add/comment/<int:food_id>', views.CommentView.as_view()),
    path('get/favorite/food', views.FavoriteFoodView.as_view()),

]
