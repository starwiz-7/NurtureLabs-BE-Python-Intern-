from .views import *
from django.urls import path
from advisor.views import *

urlpatterns = [
    path('register/',RegistrationView.as_view(), name='user_register'),
    path('login/',LoginView.as_view(), name='user_login'),
    path('<int:id>/advisor/', allAdvisorView.as_view(), name='list_advisors'),
    path('<int:user_id>/advisor/<int:advisor_id>/', bookAdvisorView.as_view(), name='book_advisors'),
    path('<int:user_id>/advisor/booking/',allBookingsView.as_view())
]