from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('change-contact/', views.ChangeAddress.as_view(), name='change-contact'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    
    path('profile/', views.CurrentProfileView.as_view(), name='personal-profile'),
    path('profile/<slug:username>/', views.ProfileView.as_view(), name='user-profile'),
]
