from django.contrib import admin
from django.urls import path , include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',include('article.urls'))
]

admin.site.site_title = "Article"
admin.site.site_header = "Article Admin"
admin.site.site_title = 'Article Admin Area'
