from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('auth/users/activate/<str:uidb64>/<str:token>/', views.ActivateUserView.as_view(), name='custom_activation'),
]