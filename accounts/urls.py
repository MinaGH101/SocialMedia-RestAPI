from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_token

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserReisterView.as_view(), name="register"),
    path('api-token-auth/', auth_token.obtain_auth_token),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:id>', views.UserProfileView.as_view(), name='profile'),
    path('reset/', views.UserResetPassword.as_view(), name='reset_password'),
    path('follow/<int:user_id>', views.UserFollowView.as_view(), name='follow'),
    path('unfollow/<int:user_id>', views.UserUnfollowView.as_view(), name='unfollow'),
    path('profile/', views.EditProfileView.as_view(), name='edit_profile'),
]

