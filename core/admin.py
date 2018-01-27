from django.contrib import admin

# Register your models here.
from .models import product, links, tags, adverts, email_list, product_catagory

class ProductAdmin(admin.ModelAdmin):
	list_display = ['user', 'product_name']
	list_filter = ['user', 'product_name']
	search_fields = ['user', 'product_name']
	filter_horizontal = ['tag', 'twin']

class TagAdmin(admin.ModelAdmin):
	list_display = ['tag']
	list_filter = ['tag']
	search_fields = ['tag']

class LinksAdmin(admin.ModelAdmin):
	list_display = ['user','social_connection', 'link']
	list_filter = ['user','social_connection', 'link']
	search_fields = ['user','social_connection', 'link']

class AdvertAdmin(admin.ModelAdmin):
	list_display = ['user', 'customer','advert_status','advert_view', 'current_clicks', 'advert_lifespan']
	list_filter = ['user', 'customer','advert_status','advert_view', 'current_clicks', 'advert_lifespan']
	search_fields = ['user', 'customer','advert_status','advert_view', 'current_clicks', 'advert_lifespan']

class EmailAdmin(admin.ModelAdmin):
	list_display = ['email', 'timestamp','updated',]
	list_filter = ['email', 'timestamp','updated',]
	search_fields = ['email', 'timestamp','updated',]

class ProductCatAdmin(admin.ModelAdmin):
	list_display = ['catagory_name', 'catagory_pitch']
	list_filter = ['catagory_name', 'catagory_pitch']
	search_fields = ['catagory_name', 'catagory_pitch']


admin.site.register(adverts, AdvertAdmin)
admin.site.register(tags, TagAdmin)
admin.site.register(product, ProductAdmin)
admin.site.register(links, LinksAdmin)
admin.site.register(email_list, EmailAdmin)
admin.site.register(product_catagory, ProductCatAdmin)

