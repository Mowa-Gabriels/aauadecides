from django.urls import path
from . import views

urlpatterns = [
     #path('home/', views.home, name='home'),
      path('login/', views.login_user, name='login'),
       path('logout/', views.logout_user, name='logout'),
       path('validate_login/', views.login_validate, name='login_validate'),
       path('validate_otp/', views.validate_otp, name='validate_otp'),
       path('otp/', views.generate_and_send_otp, name='otp_page'),

      path('', views.poll_page, name='poll_page'),
      path('poll_detail/<poll_id>/', views.poll_detail, name='poll_detail'),
      path('create/poll/', views.add_poll, name='poll_add'),
      path('poll_edit/<poll_id>/', views.poll_edit, name='poll_edit'),
      path('details/<poll_id>/vote/', views.vote_poll, name='vote'),
      path('delete/poll/<poll_id>/', views.poll_delete, name='delete'),
      path('poll/<poll_id>/choice/add', views.add_choice, name='add_choice'),
      path('choice_edit/<choice_id>/', views.choice_edit, name='choice_edit'),
      path('delete/poll/choice/<choice_id>/', views.choice_delete, name='delete_choice'),
      path('poll/<poll_id>/result', views.poll_result, name='result'),


]



from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



