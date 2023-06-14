from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import transport as qr
urlpatterns = [
    path('', views.home, name='home'),
    path('transport/', views.transport, name='transport'),
    path('personal/', views.personal, name='personal'),
    path('support/', views.support, name='support'),
    path('anketa/', views.anketa, name ='anketa'),
    path('bay/', qr, name='bay'),
    path('<int:pk>/update_transport', views.TransportUpdateView.as_view(), name ='transport-update'),
    path('<int:pk>/delete_transport', views.TransportDeleteView.as_view(), name ='transport-delete'),
    path('<int:pk>/delete_home', views.HomeDeleteView.as_view(), name ='home-delete'),
    path('<int:pk>/update_home', views.HomeUpdateView.as_view(), name ='home-update'),
    path('<int:pk>/update_personal', views.PersonalUpdateView.as_view(), name ='personal-update'),
    path('<int:pk>/delete_personal', views.PersonalDeleteView.as_view(), name ='personal-delete'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)