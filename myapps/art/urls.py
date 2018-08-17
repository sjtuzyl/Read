from django.conf.urls import url
from art import views

urlpatterns = [
    url(r'^show/(\d+?)/',views.show),
    url(r'^qd/(\d+?)/',views.qdArticl),
    url(r'^query_qd/(\d+?)/',views.queryQDState)
]