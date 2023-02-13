from django.urls import path
from account.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, \
    SendPasswordResetEmailView, UserPasswordResetView, UpdateRegisterUserView, lobby, ScanDataViewSet

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-user-type/', UpdateRegisterUserView.as_view(), name='update-user-type'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('scan-data/', ScanDataViewSet.as_view(), name='scan-data'),
    path('lobby/', lobby, name='lobby'),
]