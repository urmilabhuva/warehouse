
#!python
# authtest/urls.py
from django.conf.urls import include, url
from django.contrib import admin
# Add this import
from django.contrib.auth import views
from dashboard import urls as dashboard_url
# Add this import
from dashboard.forms import LoginForm
from dashboard.api.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include(dashboard_url)),
    url(r'^$', views.login, {'template_name': 'components/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^admin/login', views.login, {'template_name': 'components/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),

    #api
    url(r'^warehouselist', Warehouselist.as_view(),),
    url(r'^storelist/(?P<warehouse>.+)', Storelist.as_view()),
    url(r'^getfirstrecord/(?P<user_id>.+)/s_id/(?P<s_id>.+)/w_id/(?P<w_id>.+)/picklist/(?P<picklist>.+)', getfirstrecord.as_view() ),
    url(r'^getpicklist/(?P<s_id>.+)', getpicklist.as_view(), ),
    url(r'^getproduct/bin_location/(?P<bin_location>.+)/barcode_num/(?P<barcode_num>.+)/user_id/(?P<user_id>.+)/s_id/(?P<s_id>.+)/w_id/(?P<w_id>.+)', getproduct.as_view(), ),
    url(r'^gettotereport/(?P<user_id>.+)/tote/(?P<tote>.+)', getreport.as_view(), ),
    url(r'^scanner/login/username/(?P<username>.+)/password/(?P<password>.+)/device_token/(?P<dtoken>.+)/device/(?P<did>.+)', userlogin.as_view(), ),
    url(r'^nextproduct/product_id/(?P<product_id>.+)/user_id/(?P<user_id>.+)/picklist/(?P<picklist>.+)/bin_location/(?P<bin_location>.+)', getnextproduct.as_view(), ),
    url(r'^productupdate/product_id/(?P<product_id>.+)/barcode_num/(?P<barcode_num>.+)/quntity/(?P<quntity>.+)/bin_location/(?P<bin_location>.+)/user_id/(?P<user_id>.+)/tote/(?P<tote>.+)/picklist/(?P<picklist>.+)', UpdateProduct.as_view(),),
    url(r'^previousproduct/product_id/(?P<product_id>.+)/user_id/(?P<user_id>.+)/picklist/(?P<picklist>.+)/bin_location/(?P<bin_location>.+)', getpreviousproduct.as_view(), ),
    url(r'^sfo', SFOData.as_view(),),
]
