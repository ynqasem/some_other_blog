from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include('posts.urls', namespace="posts")),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^api/', include('api.urls', namespace="api")),
    url(r'^google_app/', include('google_app.urls', namespace="google_app")),
    url(r'^github_app/', include('github_app.urls', namespace="github_app")),
    url(r'^twitter_app/', include('twitter_app.urls', namespace="twitter_app")),
    url(r'^accounts/', include('allauth.urls')),
]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)