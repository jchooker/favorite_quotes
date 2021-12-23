from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def curr_user(request):
    return User.objects.get(id=request.session['user_id'])

def curr_quote(request, quote_id):
    return Quote.objects.get(id=quote_id)

def index(request):
    return render(request, "login_reg.html")

def reg(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="reg")
            return redirect('/')
        else:
            user = User.objects.create(
                f_name = request.POST['f_name'],
                l_name = request.POST['l_name'],
                email = request.POST['email'],
                pw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['user_id'] = user.id
            return redirect('/dashboard')
    else:
        return redirect('/')

def log_in(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="log")
            return redirect('/')
        user = User.objects.get(email=request.POST['email2'])
        request.session['user_id'] = user.id
    else:
        return redirect('/')
    return redirect('/dashboard')

def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Only logged-in users can view this site')
        return redirect('/')
    else:
        context = {
            'quotes':Quote.objects.all(),
            'user':curr_user(request)
        }   
    return render(request, 'dashboard.html', context)

def add_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="addq")
            return redirect('/dashboard')
        user = curr_user(request)
        quote = Quote.objects.create(
            quote_txt = request.POST['quote_txt'],
            attr_author = request.POST['attr_author'],
            uploaded_by = user
        )
        quote.users_who_like.add(user)
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

def edit_self(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user':user,
    }
    return render(request, "view_user_admin.html", context)

def update_user(request):
    if request.method == "POST":
        user=curr_user(request)
        errors = User.objects.update_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="update")
            return redirect(f'/myaccount/{user.id}')
        else:
            user=curr_user(request)
            user.f_name = request.POST['f_name']
            user.l_name = request.POST['l_name']
            user.email = request.POST['email']
            user.save()
            return redirect('/dashboard')
    else:
        return redirect('/')

def view_other_user(request, user_id):
    context = {
        'user':User.objects.get(id=user_id),
        'quotes':Quote.objects.all()
    }
    return render(request, "view_other_user.html", context)

def like(request, quote_id):
    user = curr_user(request)
    quote = curr_quote(request, quote_id)
    user.liked_quotes.add(quote)

    return redirect('/dashboard')

def unlike(request, quote_id):
    user = curr_user(request)
    quote = curr_quote(request, quote_id)
    user.liked_quotes.remove(quote)

    return redirect('/dashboard')

def delete(request, quote_id):
    quote = curr_quote(request, quote_id)
    quote.delete()
    return redirect('/dashboard')

def log_out(request):
    request.session.flush()
    return redirect('/')
