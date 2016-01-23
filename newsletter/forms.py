from django import forms

from .models import SignUp

class SignUpForm(forms.ModelForm):
	class Meta:
		model = SignUp
		fields = ['full_name', 'email']

	# A python method for validating email addresses
	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_base, provider = email.split("@")
		domain, extension = provider.split(".")
		if not extension == "edu":
			raise forms.ValidationError("Please enter a .edu email")
		# if not domain == "harvard":
		# 	raise forms.ValidationError("Please enter a harvard email")
		return email

	def clean_full_name(self):
		full_name = self.cleaned_data.get('full_name')
		# if full_name == "":
		# 	raise forms.ValidationError("Name cannot be empty.")
		# symbols = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
		# for i in full_name:
		# 	if i in symbols:
		# 		raise forms.ValidationError("Name cannot contain symbols.")
		return full_name

class ContactForm(forms.Form):
	full_name = forms.CharField(required = False)
	email = forms.CharField()
	message = forms.CharField()
