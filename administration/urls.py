
from django.urls import path
from . import views


urlpatterns = [
   path('', views.info_list, name='info_list'),
   path('add_position/', views.add_position, name='add_pos'),
   path('edit_position/<poss_id>', views.edit_position, name='edit_pos'),
   path('delete_position/<poss_id>', views.delete_position, name='delete_pos'),
   path('candidate/info/<poss_id>/', views.info_detail, name='info_detail'),
   path('candidate/info/create/<poss_id>/', views.add_info, name='add_info'),
   path('edit_candidate_info/<candidate_id>', views.edit_candidate_info, name='edit_candidate'),

   path('MakE_coMPlainT/', views.send_complaint, name='send_complaint'),
   path('SenDuPDAteS/', views.send_update, name='send_update'),

   path('voter_info/.csv_upload', views.import_csv, name='import'),
    path('voter_info/.csv_download', views.export, name='export'),
     path('voter_info/.pdf_download', views.render_pdf_view, name='pdf_export'),



   ]


from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


