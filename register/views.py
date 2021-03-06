from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.forms.models import inlineformset_factory
import requests as r
import json

from companies.models import Company, CompanyContact
from orders.models import Product, Order, ProductType, ElectricityOrder
from exhibitors.models import Exhibitor, TransportationAlternative
from fair.models import Fair
from matching.models import Survey

from .models import SignupContract, SignupLog

from .forms import CompleteCompanyDetailsForm, CompleteLogisticsDetailsForm, CompleteCatalogueDetailsForm, NewCompanyForm, CompleteProductQuantityForm, CompleteProductBooleanForm, CompleteFinalSubmissionForm, RegistrationForm, ChangePasswordForm
from orders.forms import get_order_forms, ElectricityOrderForm
from exhibitors.forms import ExhibitorProfileForm, TransportationForm
from matching.forms import ResponseForm
from companies.forms import CompanyForm, CompanyContactForm, CreateCompanyContactForm, CreateCompanyContactNoCompanyForm, UserForm
from transportation.forms import PickupForm, DeliveryForm
from accounting.models import Product, Order, RegistrationSection


from .help.methods import get_time_flag


def choose_company(request):
	if not request.user.is_authenticated():
		fair = Fair.objects.filter(current = True).first()
		return render(request, 'register/outside/login_or_register.html')
	
	company_contacts = CompanyContact.objects.filter(user = request.user).exclude(company = None)
	
	if len(company_contacts) == 1: return redirect('anmalan:form', company_contacts.first().company.pk)
	
	return render(request, 'register/choose_company.html', {'company_contacts': company_contacts})


def form(request, company_pk):
	if not request.user.is_authenticated(): return redirect('anmalan:logout')
	
	company = get_object_or_404(Company, pk = company_pk)
	fair = Fair.objects.filter(current = True).first()
	
	if request.user.has_perm('companies.base'):
		company_contact = None
	
	else:
		company_contact = CompanyContact.objects.filter(user = request.user, company = company).first()
		
		if not company_contact: return redirect('anmalan:choose_company')
	
	if timezone.now() < fair.registration_start_date: return render(request, 'register/errors/before_initial.html')
	
	# show IR form if IR has opened and CR has not opened (=> we could be between IR and CR)
	if timezone.now() >= fair.registration_start_date and timezone.now() < fair.complete_registration_start_date: return form_initial(request, company, company_contact, fair)
	
	# we're in or after CR! perhaps the company did not complete their IR?
	signature = SignupLog.objects.filter(company = company, contract__fair = fair, contract__type = 'INITIAL')
	if len(signature) == 0: return render(request, 'register/errors/after_initial_no_signature.html')
	
	# ...or perhaps they weren't selected to participate in this year's fair?
	exhibitor = Exhibitor.objects.filter(fair = fair, company = company).first()
	if exhibitor is None: return render(request, 'register/errors/after_initial_no_exhibitor.html')
	
	return form_complete(request, company, company_contact, fair, exhibitor)


def form_initial(request, company, company_contact, fair):
	return render(request, 'register/forms/initial.html',
	{
		'fair': fair,
		'company': company,
		'company_contact': company_contact,
		'is_editable': timezone.now() >= fair.registration_start_date and timezone.now() <= fair.registration_end_date
	})


def form_complete(request, company, company_contact, fair, exhibitor):
	contract = SignupContract.objects.filter(fair = fair, type = 'COMPLETE').first()
	signature = SignupLog.objects.filter(company = company, contract__fair = fair, contract__type = 'COMPLETE').first()
	
	form_company_details = CompleteCompanyDetailsForm(request.POST if request.POST and request.POST.get('save_company_details') else None, instance = company)
	form_logistics_details = CompleteLogisticsDetailsForm(request.POST if request.POST and request.POST.get('save_logistics_details') else None, instance = exhibitor)
	form_catalogue_details = CompleteCatalogueDetailsForm(request.POST if request.POST.get('save_catalogue_details') else None, request.FILES if request.POST.get('save_catalogue_details') else None, instance = exhibitor)
	form_final_submission = CompleteFinalSubmissionForm(request.POST if request.POST and request.POST.get('save_final_submission') else None)
	
	orders = Order.objects.filter(purchasing_company = company, unit_price = None, name = None)
	
	registration_sections = []
	
	for registration_section_raw in RegistrationSection.objects.all():
		registration_section = {
			'name': registration_section_raw.name,
			'description': registration_section_raw.description,
			'products': []
		}
		
		for product_raw in Product.objects.select_related('category').filter(revenue__fair = fair, registration_section = registration_section_raw):
			quantity_initial = 0
			
			for order in orders:
				if order.product == product_raw:
					quantity_initial += order.quantity
			
			if product_raw.max_quantity == 1:
				form_product = CompleteProductBooleanForm(request.POST if request.POST and request.POST.get('save_product_' + str(product_raw.id)) else None, prefix = 'product_' + str(product_raw.id), initial = {'checkbox': True if quantity_initial == 1 else False})
			
			else:
				form_product = CompleteProductQuantityForm(request.POST if request.POST and request.POST.get('save_product_' + str(product_raw.id)) else None, prefix = 'product_' + str(product_raw.id))
				form_product.fields['quantity'].choices = [(i, i) for i in range(0, (product_raw.max_quantity + 1) if product_raw.max_quantity is not None else 21)]
				form_product.fields['quantity'].initial = quantity_initial
			
			if request.POST and request.POST.get('save_product_' + str(product_raw.id)) and form_product.is_valid():
				quantity = (1 if form_product.cleaned_data['checkbox'] else 0) if product_raw.max_quantity == 1 else int(form_product.cleaned_data['quantity'])
				
				if quantity == 0:
					for order in Order.objects.filter(purchasing_company = company, product = product_raw, unit_price = None, name = None):
						order.delete()
				
				else:
					order_all = Order.objects.filter(purchasing_company = company, product = product_raw, unit_price = None, name = None)
					
					if len(order_all) == 1:
						order = order_all.first()
						order.quantity = quantity
					
					elif len(order_all) > 1:
						for o in order:
							o.delete()
					
					if len(order_all) != 1: order = Order(purchasing_company = company, product = product_raw, quantity = quantity)
					
					order.save()
			
			product = {
				'id': product_raw.id,
				'name': product_raw.name,
				'description': product_raw.description,
				'category': product_raw.category.name if product_raw.category else None,
				'unit_price': product_raw.unit_price,
				'max_quantity': product_raw.max_quantity,
				'form': form_product
			}
			
			registration_section['products'].append(product)
		
		registration_sections.append(registration_section)
	
	if signature:
		form_catalogue_details.fields['catalogue_about'].required = True
		form_catalogue_details.fields['catalogue_purpose'].required = True
		form_catalogue_details.fields['catalogue_logo_squared'].required = True
	
	if request.POST:
		if request.POST.get('save_company_details') and form_company_details.is_valid():
			form_company_details.save()
			form_company_details = CompleteCompanyDetailsForm(instance = company)
		
		elif request.POST.get('save_logistics_details') and form_logistics_details.is_valid():
			form_logistics_details.save()
			form_logistics_details = CompleteLogisticsDetailsForm(instance = exhibitor)
		
		elif request.POST.get('save_catalogue_details') and form_catalogue_details.is_valid():
			form_catalogue_details.save()
			form_catalogue_details = CompleteCatalogueDetailsForm(instance = exhibitor)
		
		elif request.POST.get('save_final_submission') and form_final_submission.is_valid() and signature is None:
			exhibitor.accept_terms = True
			exhibitor.save()
			
			signature = SignupLog.objects.create(company_contact = company_contact, contract = contract, company = company)
	
	form_company_details.fields['invoice_name'].widget.attrs['placeholder'] = company.name
	
	orders = []
	orders_total = 0
	
	for order in Order.objects.filter(product__revenue__fair = fair, purchasing_company = company):
		unit_price = order.product.unit_price if order.unit_price is None else order.unit_price
		
		orders_total += order.quantity * unit_price
		
		orders.append(
		{
			'category': order.product.category.name if order.product.category else None,
			'name': order.product.name if order.name is None else order.name,
			'description': order.product.description if order.product.registration_section is None else None,
			'quantity': order.quantity,
			'unit_price': unit_price
		})
	
	errors = []
	
	if not company.has_invoice_address(): errors.append('Invoice address')
	if not exhibitor.booth_height: errors.append('Height of booth (cm)')
	if exhibitor.electricity_total_power is None: errors.append('Total power needed (W)')
	if exhibitor.electricity_socket_count is None: errors.append('Number of power sockets required')
	if not exhibitor.catalogue_about: errors.append('Short text about the company')
	if not exhibitor.catalogue_purpose: errors.append('Text about the purpose of the company')
	if not exhibitor.catalogue_logo_squared: errors.append('Squared logotype')
	
	if signature:
		for field in form_company_details.fields: form_company_details.fields[field].disabled = True
		for field in form_logistics_details.fields: form_logistics_details.fields[field].disabled = True
	
	return render(request, 'register/forms/complete.html',
	{
		'fair': fair,
		'contract': contract,
		'company': company,
		'company_contact': company_contact,
		'form_company_details': form_company_details,
		'form_logistics_details': form_logistics_details,
		'form_catalogue_details': form_catalogue_details,
		'registration_sections': registration_sections,
		'orders': orders,
		'orders_total': orders_total,
		'errors': errors,
		'form_final_submission': form_final_submission,
		'signature': signature,
		'is_editable': timezone.now() >= fair.complete_registration_start_date and timezone.now() <= fair.complete_registration_close_date
	})


def create_user(request, template_name='register/outside/create_user.html'):
	contact_form = CreateCompanyContactForm(request.POST or None, prefix='contact')
	user_form = UserForm(request.POST or None, prefix='user')
	
	if request.POST and contact_form.is_valid() and user_form.is_valid():
		user = user_form.save(commit=False)
		contact = contact_form.save(commit=False)
		user.username = contact.email_address
		user.email = contact.email_address
		user.save()
		contact.user = user
		contact.save()
		user = authenticate(username=contact_form.cleaned_data['email_address'], password=user_form.cleaned_data['password1'],)
		login(request, user)
		return redirect('anmalan:choose_company')
	
	return render(request, template_name, dict(contact_form=contact_form, user_form=user_form))


def create_company(request, template_name='register/outside/create_company.html'):
	form = NewCompanyForm(request.POST or None)
	contact_form = CreateCompanyContactNoCompanyForm(request.POST or None, prefix='contact')
	user_form = UserForm(request.POST or None, prefix='user')
	
	if contact_form.is_valid() and user_form.is_valid() and form.is_valid():
		company = form.save()
		user = user_form.save(commit=False)
		contact = contact_form.save(commit=False)
		user.username = contact.email_address
		user.email = contact.email_address
		user.save()
		contact.user = user
		contact.confirmed = True #Auto confirm contacts who register a new company
		contact.company = company
		contact.save()
		user = authenticate(username=contact_form.cleaned_data['email_address'], password=user_form.cleaned_data['password1'],)
		login(request, user)
		return redirect('anmalan:choose_company')
	return render(request, template_name, dict(form=form, contact_form=contact_form, user_form=user_form))


def change_password(request, template_name='register/change_password.html'):
	if request.method == 'POST':
		form = ChangePasswordForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('anmalan:choose_company')
		else:
			return redirect('anmalan:change_password')
	else:
		form = ChangePasswordForm(user=request.user)
	
	return render(request, template_name, {'form':form})


def preliminary_registration(request, fair, company, contact, contract, exhibitor, signed_up, allow_saving):
	form = RegistrationForm((request.POST or None) if allow_saving else None, prefix = 'registration', instance = company)
	
	if not signed_up and form.is_valid():
		form.cleaned_data["groups"] = company.groups.filter(fair = fair).union(form.cleaned_data["groups"])
		form.save()
		SignupLog.objects.create(company_contact = contact, contract = contract, company = contact.company)
		
		return redirect('anmalan:choose_company')
	
	return ('register/registration.html', dict(registration_open = True, signed_up = signed_up, contact = contact, company=company, exhibitor = exhibitor, fair=fair, form = form, contract_url = contract.contract.url if contract else None ))
