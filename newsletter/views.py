from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import SignUpForm, ContactForm
from .models import SignUp

def home(request):
	title = "Sign Up Now"
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
	if request.user.is_authenticated() and request.user.is_staff:
		# print (SignUp.objects.all())
		# i  = 1
		# for instance in SignUp.objects.all():
		# 	print i
		# 	print (instance)
		# 	print (instance.full_name)
		# 	i+=1
		# queryset = SignUp.objects.all().order_by('-timestamp').filter(email__icontains="harvard")
		queryset = SignUp.objects.all().order_by('-timestamp')
		context = {
				"queryset": queryset
		}
	

	return render(request, "home.html", context)


def contact(request):
	title = 'Contact Us'
	title_align_center = True
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
		"title": title,
		"title_align_center": title_align_center,
	}
	return render(request, "forms.html", context)
