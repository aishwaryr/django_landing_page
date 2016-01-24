from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import SignUpForm, ContactForm

def home(request):
	title = "Welcome"
	form = SignUpForm(request.POST or None)
	context = {
			   "title": title,
			   "form": form	
	}

	#this validates according to validators in forms.py
	if form.is_valid():
		# form.save()
		# print request.POST[' email'] # not recommended
		instance = form.save(commit=False)

		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "Anonymous"
		instance.full_name = full_name
		# if not instance.full_name:
		# 	instance.full_name = "Anonymous"
		instance.save()
		context = {
					"title": "Thank You"
		}



	return render(request, "home.html", context)


def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.iteritems():
		# 	print key, value
		# 	#print form.cleaned_data.get(key)
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		# print email, message, full_name
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email,'otheremail@email.com']
		contact_message = "%s: %s via %s" %(
						form_full_name,
						form_message,
						form_email)
		
		send_mail(subject, 
				contact_message, 
				from_email,
				to_email,
				fail_silently=False)

	context = {
		"form": form,
	}
	return render(request, "forms.html", context)
