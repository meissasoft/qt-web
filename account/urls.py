from django.urls import path
from account.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, \
    SendPasswordResetEmailView, UserPasswordResetView, UpdateRegisterUserView, lobby, ScanDataView, UserConnectionView, \
    IsScanView, SysInfoView, ItgnirDataView, ModelTrainingView, PredictView, ModelTrainingView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-user-type/', UpdateRegisterUserView.as_view(), name='update-user-type'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('scan-data/', ScanDataView.as_view(), name='scan-data'),
    path('is-scan/', IsScanView.as_view(), name='is-scan'),
    path('user-connection/', UserConnectionView.as_view(), name='user-connection'),
    path('sys-info/', SysInfoView.as_view(), name='sys-info'),
    path('itgnir-data/', ItgnirDataView.as_view(), name='itgnir-data'),
    path('model-training/', ModelTrainingView.as_view(), name='model-training'),
    path('prediction/', PredictView.as_view(), name='prediction'),
    path('lobby/', lobby, name='lobby'),
]
