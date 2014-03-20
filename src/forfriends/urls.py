from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from userprofile.views import signup

urlpatterns = patterns('',	
    # Examples:
    # url(r'^$', 'forfriends.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'userprofile.views.signup'),
    url(r'^profile_home$', 'userprofile.views.home'),
    url(r'^logged_in$', 'userprofile.views.login_view'),
    url(r'^profile_view$', 'userprofile.views.profile_view'),
    url(r'^interests$', 'userprofile.views.interests'),
    url(r'^pictures$', 'userprofile.views.pictures'),

    #url(r'^test/$', 'userprofile.views.registration'),
    #url(r'submit', 'userprofile.views.registration'),
    
)
