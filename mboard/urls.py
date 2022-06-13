from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from mboard.views import *

urlpatterns = [
    path('', list_threads, name='list_threads'),
    path('thread/<int:thread_id>/', get_thread, name='get_thread'),
    path('test/', testview, name='testview')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
