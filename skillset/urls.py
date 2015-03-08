from django.conf.urls import patterns, include, url
from django.contrib import admin
from skills import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skillset.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','skills.views.index',name='index'),
    url(r'^newskill/$','skills.views.newskill',name='newskill'),
    url(r'^allskill/$','skills.views.allskill',name='allskill'),
    url(r'^deleteskill/$','skills.views.deleteskill',name='deleteskill'),


)
