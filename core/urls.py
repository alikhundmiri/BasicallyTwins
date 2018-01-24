"""dlauncher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """

from django.urls import path, include
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.lander , name='lander'),
	path('products/', views.index, name='home'),
    path('ads/<int:id>/', views.advert_redirect, name='advert_redirect'),    

    path('@<str:username>/', include([
        path('', views.user_profile, name='user_profile'),
        path('create_product', views.create_product, name='create_product'),
        path('edit_product', views.edit_product, name='edit_product'),
        path('all_advert', views.all_advert, name='all_advert'),
        path('create_advert', views.create_advert, name='create_advert'),
        path('edit_advert', views.edit_advert, name='edit_advert'),
        ])),
    # path('new', views.card_create, name='card_create'),
    # path('news', views.fetch_news, name='fetch_news'),
	
    path('tags/', include([
		path('', views.all_tags, name='all_tags'),
		path('<slug:slug>/', views.tag_detail, name='tag_detail'),
		])),

    path('<slug:slug>/', views.product_detail, name='product_detail'),

]

