
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# An example from joinCFE

def validate_domainonly_email(value):
    """
    Let's validate the email passed is in the domain "yourdomain.com"
    """
    if not "yourdomain.com" in value:
        raise ValidationError(_"Sorry, the email submitted is invalid. All emails have to be registered on this domain only.", status='invalid')


# My custom validator
def validate_product_name(value):
	"""
	take the 'value' and see if it contain 
		atleast 3 letters
		no spacial characters except '-'

	"""
	pass

