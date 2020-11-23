
from django.urls import path
from . import views
from .views import VoterSignUp,AdminSignUp

urlpatterns = [
         path('voters_page/', views.voters_page, name='voters_page'),

         path('voter_signup/', VoterSignUp.as_view(), name='voter_signup'),
         path('admin_signup/', AdminSignUp.as_view(), name='admin_signup'),


   ]