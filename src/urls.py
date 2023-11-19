from django.urls import path
from .views import *


urlpatterns = [
    path('', home , name="home"),
    path('register/', register , name="register"),
    path('user-login/', user_login , name="user-login"),
    path('log-out/', log_out , name="log-out"),
    path('add-subscription/', add_subscription , name="add_subscription"),
    path('blog-view/<int:pk>', blog_view , name="blog_view"),
    path('filter_by_category/<int:id>/', filter_by_category , name="filter_by_category"),
    path('add-blog/', add_blog , name="add-blog"),
    path('profile/', profile , name="profile"),
    path('update-profile/<int:pk>/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('update-blog/<str:pk>/',update_blog,name="update-blog"),
    path('delete-blog/<str:pk>/',delete_blog,name="delete-blog"),
]
