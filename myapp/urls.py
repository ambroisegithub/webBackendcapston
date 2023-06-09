from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items/',views.MenuItemView.as_view()),
    path('menu-items/<int:pk>',views.SingletMenuItemView.as_view()),
    path('menu-item/', views.menu_items),
    path('api-token-auth/',obtain_auth_token),
    path('signup/', views.UserSignupView.as_view()),
    path('login/', views.UserLoginView.as_view(),name='login'), 
    path('users/', views.UserListView.as_view()), 
]
