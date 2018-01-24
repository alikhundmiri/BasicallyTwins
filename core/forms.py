from django import forms
from django.forms.formsets import BaseFormSet

from .models import product, adverts, tags, links, email_list
# from pagedown.widgets import PagedownWidget

# form to create a new product
class ProductForm(forms.ModelForm):
    twin = forms.ModelMultipleChoiceField(queryset = product.objects.all(), widget=forms.CheckboxSelectMultiple())

    # tags = forms.ModelMultipleChoiceField(queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = product
        fields = [
        "product_name",
        "product_pitch",
        "monthly_revenue",
        "website",
        "twin",
            ]
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["twin"].required = False 

# form to create a new product
class EmailForm(forms.ModelForm):
    class Meta:
        model = email_list
        fields = [
        "email",
        ]
# form to create advert
class AdvertForm(forms.ModelForm):

    class Meta:
        model = adverts;
        fields = [
        "customer",
        "ad_words",
        "advert_text",
        "image",        
        "advert_lifespan",
        ]



# class BaseLinkFormSet(BaseFormSet):
#     def clean(self):
#         """
#         Adds validation to check that no two links have the same anchor or URL
#         and that all links have both an anchor and URL.
#         """
#         if any(self.errors):
#             return

#         anchors = []
#         urls = []
#         duplicates = False

#         for form in self.forms:
#             if form.cleaned_data:
#                 anchor = form.cleaned_data['title']
#                 url = form.cleaned_data['link']

#                 # Check that no two links have the same anchor or URL
#                 if anchor and url:
#                     if anchor in anchors:
#                         duplicates = True
#                     anchors.append(anchor)

#                     if url in urls:
#                         duplicates = True
#                     urls.append(url)

#                 if duplicates:
#                     raise forms.ValidationError(
#                         'Links must have unique Names and URLs.',
#                         code='duplicate_links'
#                     )

#                 # Check that all links have both an anchor and URL
#                 if url and not anchor:
#                     raise forms.ValidationError(
#                         'All links must have an anchor.',
#                         code='missing_anchor'
#                     )
#                 elif anchor and not url:
#                     raise forms.ValidationError(
#                         'All links must have a URL.',
#                         code='missing_URL'
#                     )
