from django.shortcuts import render, redirect
from django.db import connection
from .models import User, Note


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # FLAW 5: A07 Identification and Authentication Failures - no password requirements
        # FIX: uncomment the lines below to enforce minimum password length
        # if len(password) < 8:
        #     return render(request, 'notes_app/register.html', {'error': 'Password must be at least 8 characters'})
        # FLAW 3: A02 Cryptographic Failures - storing password in plaintext
        # FIX: Use Django's built-in auth: User.objects.create_user(username, password=password)
        User.objects.create(username=username, password=password)
        return redirect('/login/')
    return render(request, 'notes_app/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # FLAW 3: Comparing plaintext passwords
        # FIX: Use Django's authenticate() which handles hashed passwords
        try:
            user = User.objects.get(username=username, password=password)
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


# FLAW 2: A01 Broken Access Control
# Any logged in user can view any note by changing the note id in the URL
# FIX: Check that the note belongs to the logged in user before returning it
def view_note(request, note_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    # FLAW: No ownership check - any user can view any note
    note = Note.objects.get(id=note_id)
    # FIX:
    # if note.user.id != int(user_id):
    #     return redirect('/notes/')
    return render(request, 'notes_app/view_note.html', {'note': note})


# FLAW 1: A03 Injection - SQL injection in search
# User input is inserted directly into raw SQL query
# FIX: Use Django ORM: Note.objects.filter(user=user, title__icontains=query)
def search(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    query = request.GET.get('q', '')
    user = User.objects.get(id=user_id)
    # FLAW: Raw SQL with unsanitized input
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, title, content FROM notes_app_note WHERE user_id = "
            + str(user_id)
            + " AND title LIKE '%" + query + "%'"
        )
        rows = cursor.fetchall()
    notes = [{'id': r[0], 'title': r[1], 'content': r[2]} for r in rows]
    # FIX:
    # notes = Note.objects.filter(user=user, title__icontains=query)
    return render(request, 'notes_app/search.html', {'notes': notes, 'query': query})


def logout_view(request):
    request.session.flush()
    return redirect('/login/')