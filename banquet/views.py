from django.forms import modelform_factory
from django.http import  HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .models import BanquetteAttendant, BanquetTable
from exhibitors.models import Exhibitor
from .forms import BanquetteAttendantForm, ExternalBanquetSignupForm
from django.urls import reverse
from fair.models import Fair
from accounts.views import external_create_account
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
import banquet.functions as func


def sit_attendants(request, year):
    '''
    A fake button redirection target for fairs/{YEAR}/banquer 'sit attendants' button.
    Will call a function and redirect back to the banquet.
    '''
    if request.user.has_perm('banquet.can_seat_attendants'):
        func.sit_attendants()
        return HttpResponseRedirect(reverse('banquet', kwargs={'year': year }))
    else:
        return HttpResponseForbidden()

@permission_required('banquet.base')
def banquet_attendants(request, year, template_name='banquet/banquet_attendants.html'):
    """
    banquet_attendants is in url fairs/year/banquet
    Here you can see all the BanquetteAttendant objects in a table view.
    The user need the banquet.base permission to see this page
    """
    fair = get_object_or_404(Fair, year=year)
    
    banquet_attendants = BanquetteAttendant.objects.filter(fair=fair)
    return render(request, template_name, {
        'banquet_attendants': banquet_attendants,
        'fair': fair
    })
    #return render(request, 'login.html', {'next': next, 'fair': fair})


def banquet_attendant(request, year, pk, template_name='banquet/banquet_attendant.html'):
    """
    banquet_attendant is in url fairs/year/banquet/attendant/pk
    Here you can view and edit a specific BanquetteAttendant object in a form view.
    The user need the view.banquet_edit_permission permission to see this page
    """
    fair = get_object_or_404(Fair, year=year)
    banquet_attendant = get_object_or_404(BanquetteAttendant, fair=fair, pk=pk)

    exhibitors = Exhibitor.objects.filter(fair=fair)
    banquet_attendants = BanquetteAttendant.objects.filter(fair=fair)
    tables = BanquetTable.objects.filter(fair=fair)

    users_all = User.objects.all()
    forbidden_users = []
    for b in banquet_attendants:
        if b.user:
            forbidden_users.append(b.user)

    if banquet_attendant.user is not None:
        users = [banquet_attendant.user] + [u for u in users_all if u not in forbidden_users]
    else:
        users = [u for u in users_all if u not in forbidden_users]

    if request.user.is_authenticated() and request.user.has_perm('banquet.banquet_edit_permission'):
        form = BanquetteAttendantForm(
            request.POST or None,
            instance=banquet_attendant,
            users=users,
            exhibitors=exhibitors,
            tables=tables,
        )
        if form.is_valid():
            banquet_attendant = form.save(commit=False)
            banquet_attendant.fair = fair
            #banquet_attendant.user = form.cleaned_data['users_choice']
            banquet_attendant.save()
            return render(request, template_name, {'form': form, 'fair': fair })
        return render(request, template_name, {'form': form, 'fair': fair })

    else:
        return HttpResponseForbidden()


def new_banquet_attendant(request, year, template_name='banquet/banquet_attendant.html'):
    """
    new_banquet_attendant is in url fairs/year/banquet/attendant/new
    Here you can create a new BanquetteAttendant object in a form view.
    The user need the banquet.banquet_edit_permission permission to see this page
    """
    fair = get_object_or_404(Fair, year=year)

    banquet_attendants = BanquetteAttendant.objects.filter(fair=fair)
    exhibitors = Exhibitor.objects.filter(fair=fair)
    tables = BanquetTable.objects.filter(fair=fair)

    users_all = User.objects.all()
    forbidden_users = []
    for b in banquet_attendants:
        if b.user:
            forbidden_users.append(b.user)

    users = [u for u in users_all if u not in forbidden_users]

    if request.user.is_authenticated() and request.user.has_perm('banquet.banquet_edit_permission'):
        form = BanquetteAttendantForm(
            request.POST or None,
            instance=None,
            users=users,
            exhibitors=exhibitors,
            tables=tables,
        )
        if form.is_valid():
            banquet_attendant = form.save(commit=False)
            banquet_attendant.fair = fair
            #banquet_attendant.user = User.objects.get(pk=form.cleaned_data['users_choice'])
            banquet_attendant.save()
            return HttpResponseRedirect(reverse('banquet_attendants', kwargs={'year': fair.year }))
        return render(request, template_name, {'form': form, 'fair': fair })

    else:
        return HttpResponseForbidden()
      

def table_placement(request, year, template_name='banquet/table_placement.html'):
    """
    A view for viewing a user's personal table placement
    """

    fair = get_object_or_404(Fair, year=year)

    if request.user.is_authenticated():
        try:
            banquet_attendant = BanquetteAttendant.objects.get(user=request.user, fair=fair)
        except BanquetteAttendant.DoesNotExist:
            # if no attendant go to signup
            return redirect('/fairs/' + year + '/banquet/signup')

        try:
            table = BanquetTable.objects.get(fair=fair, pk=banquet_attendant.table.pk)
            table_name = table.table_name
            table_mates = BanquetteAttendant.objects.filter(fair=fair, table=table, confirmed=True).exclude(pk=banquet_attendant.pk)
        except (BanquetTable.DoesNotExist, Exception) as e:
            table_name = "No table yet"
            table_mates = None
        return render(request, template_name, {'fair': fair, 'banquet_attendant': banquet_attendant, 'table_name': table_name, 'table_mates': table_mates, 'confirmed': banquet_attendant.confirmed })
    # not authenticated
    return redirect('/fairs/' + year + '/banquet/signup')
  

def banquet_external_signup(request, year, template_name='banquet/external_signup.html'):
    """
    banquet_external_signup is in url fairs/year/banquet/signup
    Here you can create a new BanquetteAttendant object in a form view as an external
    user that ahs no AIS account and no KTH account. If not logged in
    the user will be redirected to register/external/signup
    """
    fair = get_object_or_404(Fair, year=year)

    if request.user.is_authenticated():
        try:
            banquet_instance = BanquetteAttendant.objects.get(user=request.user, fair=fair)
        except BanquetteAttendant.DoesNotExist:
            banquet_instance = None

        form = ExternalBanquetSignupForm(
            request.POST or None,
            instance = banquet_instance,
        )
        if form.is_valid():
            banquet_attendant = form.save(commit=False)
            banquet_attendant.fair = fair
            banquet_attendant.user = request.user
            banquet_attendant.email = request.user.email
            banquet_attendant.save()
            return render(request, 'banquet/thank_you.html', {'fair': fair })
        return render(request, template_name, {'form': form, 'fair': fair })
    # not authenticated
    return redirect('accounts:external_login')


def thank_you(request, year, template_name='banquet/thank_you.html'):
    fair = get_object_or_404(Fair, year=year)
    return render(request, 'banquet/thank_you.html', {'fair': fair })
