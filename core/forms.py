from django import forms
from django.forms.formsets import BaseFormSet

from .models import product, adverts, tags, links, email_list, revenue_source, anon_user_detail
# from pagedown.widgets import PagedownWidget


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

# form to create a new product
class ProductForm(forms.ModelForm):
    # twin = forms.ModelMultipleChoiceField(queryset = product.objects.all(), widget=forms.CheckboxSelectMultiple())
    revenue_source = forms.ModelMultipleChoiceField(queryset = revenue_source.objects.all(), widget=forms.CheckboxSelectMultiple())
    # tags = forms.ModelMultipleChoiceField(queryset = taggers.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = product
        fields = [
        "catagory",
        "product_name",
        "product_pitch",
        "website",
        "monthly_revenue",
        "revenue_source",
        # "twin",
            ]
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # self.fields["revenue_source"].default = [0][0] 
        self.fields["revenue_source"].help_text = "Please select atleast one" 
        # self.fields["twin"].required = False 

# FORM FOR INDIVIDUAL LINKS
class NewDetailForm(forms.Form):
    contact  = forms.CharField(
                    max_length=50,
                    widget=forms.TextInput(attrs={
                            'placeholder' : 'Please enter the credentials'
                        }), 
                    required=False)

    contact_type = forms.ChoiceField(choices=anon_user_detail.CONTACTS_LIST, required=True)

class BaseDetailFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same contact or URL
        and that all links have both an contact and URL.
        """
        if any(self.errors):
            return

        contacts = []
        contact_types = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                contact = form.cleaned_data['contact']
                contact_type = form.cleaned_data['contact_type']

                # Check that no two links have the same contact or URL
                if contact and contact_type:
                    if contact in contacts:
                        duplicates = True
                    contacts.append(contact)

                    contact_types.append(contact_type)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique Names and URLs.',
                        code='duplicate_links'
                    )
"""
                # Check that all links have both an contact and URL
                if contact_type and not contact:
                    raise forms.ValidationError(
                        'All links must have an contact.',
                        code='missing_anchor'
                    )
                elif contact and not contact_type:
                    raise forms.ValidationError(
                        'All links must have a contact_type.',
                        code='missing_URL'
                    )
"""