from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'webserver.views.home', name='home'),
    url(r'^home$', 'webserver.views.home', name='home'),
    url(r'^search$', 'webserver.views.search', name='search'),
    url(r'^history$', 'webserver.views.history', name='history'),
    url(r'^historyDisease/(?P<disease>\w+)$', 'webserver.views.historyDisease', name='historyDisease'),
    url(r'^learnedKnowledge$', 'webserver.views.learnedKnowledge', name='learnedKnowledge'),
	url(r'^login$','django.contrib.auth.views.login',{'template_name':'webserver/login.html'},name='login'),
    url(r'^register$', 'webserver.views.register', name='register'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),

    url(r'^admin/', include(admin.site.urls)),
)
