from django.contrib import admin

# Register your models here.
from .models import product, links, tags, adverts, email_list, product_catagory, revenue_source, anon_user_detail, list_items

class ProductAdmin(admin.ModelAdmin):
	list_display = ['user', 'product_name', 'product_verified', 'catagory', 'no_spam']
	list_filter = ['user', 'product_name', 'product_verified' , 'catagory', 'claimable', 'no_spam']
	list_editable = ['no_spam',]
	search_fields = ['user', 'product_name','product_verified' , 'catagory', 'claimable']
	filter_horizontal = ['tag', 'twin', 'revenue_source',]

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

class RevenueSourceAdmin(admin.ModelAdmin):
	list_display = ['source',]
	list_filter = ['source',]
	search_fields = ['source',]

class AnonUserAdmin(admin.ModelAdmin):
	list_display = ['contact','contact_type', 'connected_product']
	list_filter = ['contact','contact_type', 'connected_product']
	search_fields = ['contact','contact_type', 'connected_product']

class ListAdmin(admin.ModelAdmin):
	list_display = ['user','name', 'detail', 'link', 'public_view']
	list_filter = ['user','name', 'detail', 'link', 'public_view']
	search_fields = ['user','name', 'detail', 'link', 'public_view']
	list_editable = ['public_view']


admin.site.register(list_items, ListAdmin)
admin.site.register(anon_user_detail, AnonUserAdmin)
admin.site.register(revenue_source, RevenueSourceAdmin)
admin.site.register(adverts, AdvertAdmin)
admin.site.register(tags, TagAdmin)
admin.site.register(product, ProductAdmin)
admin.site.register(links, LinksAdmin)
admin.site.register(email_list, EmailAdmin)
admin.site.register(product_catagory, ProductCatAdmin)

