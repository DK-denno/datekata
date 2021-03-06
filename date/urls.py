from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^$',views.home,name='home'),
    url(r'^profile$',views.profile,name='profile'), 
    url(r'^message/(\d+)$',views.message,name='message'),  
    url(r'^signup/$', views.signup, name='signup'),  
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^about$', views.about, name='about'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
