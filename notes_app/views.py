from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Note


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # FIX 5: enforce minimum password length
        if len(password) < 8:
            return render(request, 'notes_app/register.html', {'error': 'Password must be at least 8 characters'})
        # FIX 3: hash the password before storing
        User.objects.create(username=username, password=make_password(password))
        return redirect('/login/')
    return render(request, 'notes_app/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # FIX 3: use check_password() to compare against hashed password
        try:
            user = User.objects.get(username=username)
            if not check_password(password, user.password):
                raise User.DoesNotExist
            request.session['user_id'] = user.id
            return redirect('/notes/')
        except User.DoesNotExist:
            return render(request, 'notes_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'notes_app/login.html')


def notes_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    user = User.objects.get(id=user_id)
    notes = Note.objects.filter(user=user)
    return render(request, 'notes_app/notes.html', {'notes': notes, 'user': user})


def add_note(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        user = User.objects.get(id=user_id)
        Note.objects.create(user=user, title=title, content=content)
        return redirect('/notes/')
    return render(request, 'notes_app/add_note.html')


def view_note(request, note_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    note = Note.objects.get(id=note_id)
    # FIX 2: ownership check
    if note.user.id != int(user_id):
        return redirect('/notes/')
    return render(request, 'notes_app/view_note.html', {'note': note})


def search(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    query = request.GET.get('q', '')
    user = User.objects.get(id=user_id)
    # FIX 1: use Django ORM instead of raw SQL
    notes = Note.objects.filter(user=user, title__icontains=query)
    return render(request, 'notes_app/search.html', {'notes': notes, 'query': query})


def logout_view(request):
    request.session.flush()
    return redirect('/login/')