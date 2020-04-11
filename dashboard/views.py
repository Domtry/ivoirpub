from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from dashboard import models
from dashboard import forms
from django.http import JsonResponse
from packages.campagne_ctrl import CampagneCtrl


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if email and password:
                response = models.Account.objects.filter(email=email, password=password)
                if len(response) == 1:
                    user_auth = response[0]
                    context = {'username':user_auth.username, 'email':user_auth.email, 'user_id': user_auth.id}
                    request.session['logged_user_id'] = context
                    return redirect('/dashboard')
                else :
                    context = {
                        'error': "Nom d'utilisateur ou mot de passe incorrect !",
                        'form': form
                    }
                    return render(request, 'dashboard/login.html', context)
        else :
            return render(request, 'dashboard/login.html', {'form': form})
    form = forms.LoginForm()
    return render(request, 'dashboard/login.html', {'form': form})


def home_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        dashboard_data = []
        campagnes = models.Campagne.objects.filter(account=account)

        for item in campagnes :
            data_objectif = models.Objectif.objects.filter(campagne=item)
            dashboard_data.append({'campagne':item, 'objectif':data_objectif})   
        context = {'username':username, 'email':email, 'dashboard_data': dashboard_data}
        return render(request, 'dashboard/index.html', context)
    else :
        return redirect('/login')


def init_config(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        if request.method == 'POST':
            form = forms.FacebookAccessForm(request.POST)
            account = models.Account.objects.get(id=logged_user_id['user_id'])
            if form.is_valid():
                resp = models.Fb_Access(
                    user_lg_token=form.cleaned_data['user_lg_token'],
                    app_secret_key=form.cleaned_data['app_secret_key'],
                    app_id=form.cleaned_data['app_id'],
                    account=account
                )
                resp.save()
                return redirect('/dashboard')
            else :
                return render(request, 'dashboard/init_config_app.html', {'form': form})
        else :
            form = forms.FacebookAccessForm()
            return render(request, 'dashboard/init_config_app.html', {'form': form})
    else:
        return redirect('/login')


def registre_page(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            email = form.cleaned_data['email']
            response = models.Account.objects.filter(email=email)
            if len(response) == 1:
                user_auth = response[0]
                context = {'username':user_auth.username, 'email':user_auth.email, 'user_id': user_auth.id}
                request.session['logged_user_id'] = context
            return redirect('/init_config')
        else:
            return render(request, 'dashboard/register.html', {'form': form})
    form = forms.RegisterForm()
    return render(request, 'dashboard/register.html', {'form': form})


def campagne_detail_page(request, cmp_id):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        campagne = models.Campagne.objects.get(id=eval(cmp_id))
        data_objectif = models.Objectif.objects.filter(campagne=campagne)
        context = {'username':username, 'email':email, 'campagne': campagne, 'data_objectif': data_objectif}
        
        if request.method == 'POST':
            form = forms.ObjectifForm(request.POST)
            if form.is_valid() :
                title = form.cleaned_data['title']
                descrip = form.cleaned_data['description']
                poste_date = form.cleaned_data['poste_date']
                poste_heure = form.cleaned_data['poste_heure']
                message = form.cleaned_data['message']
                resp = models.Objectif(
                    title=title,
                    description=descrip,
                    poste_date=poste_date,
                    poste_heure=poste_heure,
                    message=message,
                    campagne=campagne)
                resp.save()
                return redirect(f'/dashboard/campagne/{cmp_id}')
            else :
                context['form'] = forms.ObjectifForm()
                return render(request, 'dashboard/detail_cmp.html', context)
        else :
            context['form'] = forms.ObjectifForm()
            return render(request, 'dashboard/detail_cmp.html', context)
    else :
        return redirect('/login')



def campagne_home_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        data = models.Campagne.objects.filter(account=account)
        context = {'username':username, 'email':email, 'data':data}

        if request.method == 'POST':
            form = forms.CampagneForm(request.POST)
            if form.is_valid() :
                title = form.cleaned_data['title']
                descrip = form.cleaned_data['description']
                start_date = form.cleaned_data['start_date']
                close_date = form.cleaned_data['close_date']
                resp = models.Campagne(
                    title=title,
                    description=descrip,
                    start_date=start_date,
                    close_date=close_date,
                    account=account
                    )
                resp.save()
                return redirect('/dashboard/campagne')
            else :
                context['form'] = form
                return render(request, 'dashboard/cmp_home.html', context)
        else :
            form = forms.CampagneForm()
            context['form'] = form
            return render(request, 'dashboard/cmp_home.html', context)
    else :
        return redirect('/login')



def forget_password_page(request):
    return render(request, 'dashboard/forget_password.html')



def edit_login_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        context = {'username':username, 'email':email}

        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                account = models.Account.objects.get(email=email)
                account.username = form.cleaned_data['username']
                account.email = form.cleaned_data['email']
                account.password = form.cleaned_data['password']
                account.save()
                user_auth = account
                session_data = {'username':user_auth.username, 'email':user_auth.email, 'user_id': user_auth.id}
                request.session['logged_user_id'] = session_data
                context['success'] = "Votre compte a bien été modifié "
                return render(request, 'dashboard/edit_login.html', context)
            else :
                context['form']= form
                return render(request, 'dashboard/edit_login.html', context)

        form = forms.RegisterForm(initial={
            'username': username,
            'email': email
        })
        context['form']= form
        return render(request, 'dashboard/edit_login.html', context)
    else :
        redirect('/login')



def edit_facebook_app(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        context = {'username':username, 'email':email}
        account = models.Account.objects.get(id=logged_user_id['user_id'])

        if request.method == 'POST':
            form = forms.FacebookAccessForm(request.POST)
            if form.is_valid():
                fb_app_data = models.Fb_Access.objects.filter(account=account)
                fb_access = fb_app_data[0]
                fb_access.user_lg_token = form.cleaned_data['user_lg_token']
                fb_access.app_secret_key = form.cleaned_data['app_secret_key']
                fb_access.app_id = form.cleaned_data['app_id']
                fb_access.save()
                context['form'] = form
                context['success'] = "Votre compte a bien été modifié "
                return render(request, 'dashboard/edit_facebk_app.html', context)
            else :
                context['form'] = form
                return render(request, 'dashboard/edit_facebk_app.html', context)

        fb_app_data = models.Fb_Access.objects.filter(account=account)
        fb_access = fb_app_data[0]
        form = forms.FacebookAccessForm(initial={
            'user_lg_token': fb_access.user_lg_token,
            'app_secret_key': fb_access.app_secret_key,
            'app_id': fb_access.app_id,
            'account': account
        })
        context['form']= form
        return render(request, 'dashboard/edit_facebk_app.html', context)
    else:
        pass



def edit_facebook_page(request, page_id):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        context = {'username':username, 'email':email}
        page_id = int(page_id)
        fb_page = models.Fb_Page.objects.get(id=page_id)

        form = forms.FacebookPageForm(initial={
            'title':fb_page.title,
            'page_id':fb_page.page_id,
            'page_lg_tk':fb_page.page_lg_tk,
        })

        if request.method == 'POST':
            form = forms.FacebookPageForm(request.POST)
            if form.is_valid() :
                fb_page.title = form.cleaned_data['title']
                fb_page.page_id = form.cleaned_data['page_id']
                fb_page.page_lg_tk = form.cleaned_data['page_lg_tk']
                fb_page.save()
                context['form'] = form
                context['success'] = "Les parametre ont bien été modifié "
                return render(request, 'dashboard/edit_facebk_page.html', context)
            else :
                context['form'] = form
                return render(request, 'dashboard/edit_facebk_page.html', context)
        else :
            context['form'] = form
            return render(request, 'dashboard/edit_facebk_page.html', context)
    else :
        return redirect('/login')



def app_config_page(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        fb_data = models.Fb_Access.objects.filter(account=account)
        fb_page = models.Fb_Page.objects.filter(fb_access=fb_data[0])
        context = {
            'username':username, 
            'email':email, 
            'data':account, 
            'fb_data': fb_data[0],
            'fb_page': fb_page}

        if request.method == 'POST':
            form = forms.FacebookPageForm(request.POST)
            if form.is_valid() :
                fb_page = models.Fb_Page(
                    title=form.cleaned_data['title'],
                    page_id=form.cleaned_data['page_id'],
                    page_lg_tk=form.cleaned_data['page_lg_tk'],
                    fb_access=fb_data[0]
                )
                fb_page.save()
                form = forms.FacebookPageForm()
                context['form'] = form
                return render(request, 'dashboard/config.html', context)
            else :
                context['form'] = form
                return render(request, 'dashboard/config.html', context)
                
        form = forms.FacebookPageForm()
        context['form'] = form
        return render(request, 'dashboard/config.html', context)
    else :
        redirect('/login')


def disconnect(request):
    if 'logged_user_id' in request.session :
        del request.session['logged_user_id']
        return redirect('/login')
    else:
        return redirect('/login')


def campagne_control_dashboard(request):
    if 'logged_user_id' in request.session :
        logged_user_id = request.session['logged_user_id']
        email = logged_user_id['email']
        username = logged_user_id['username']
        account = models.Account.objects.get(id=logged_user_id['user_id'])
        resp = CampagneCtrl.operation_posted(account)        
        data = {
            "statu":"success",
            "message": resp
            }
        return JsonResponse(data)
    else:
        return redirect('/login')