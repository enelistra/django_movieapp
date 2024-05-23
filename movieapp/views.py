from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages, auth
from movieapp.forms import UpdateForm
from movieapp.models import movies
from django.contrib.auth import logout
from django.db.models import Q
from .models import reply, reviews, watchlist
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        cpass=request.POST.get('cfmpass')
        if password==cpass:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already exists')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return render(request,'login.html')
        else:
            messages.info(request,'password not matching')
            return render(request,'register.html')
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.error(request,'invalid username or password')
            return render (request,'login.html')
    return render(request,'login.html')

def index(request):
    obj = movies.objects.all()
    user=request.user
    person = user.username
    return render(request,'index.html',{'obj':obj,'person':person})            

# def details(request, movie_id):
#     mymovie = movies.objects.get(id=movie_id)
#     user = request.user
#     person = user.username
#     reviews_list = reviews.objects.filter(movie=mymovie).prefetch_related('replies') 
#     return render(request, 'details.html', {'movie': mymovie, 'user': user, 'reviews': reviews_list,'person':person})

@login_required
def details(request, movie_id):
    mymovie = get_object_or_404(movies, id=movie_id)
    user = request.user
    person = user.username
    reviews_list = reviews.objects.filter(movie=mymovie).order_by('-id').prefetch_related('replies') 
    is_in_watchlist = watchlist.objects.filter(user=user, movie=mymovie).exists()
    if request.method == 'POST':
        if not is_in_watchlist:
            watchlist_obj = watchlist(user=user, movie=mymovie)
            watchlist_obj.save()
            messages.success(request, 'Added to Watchlist successfully!')
            return redirect('details', movie_id=movie_id)
        else:
            messages.info(request, 'Movie is already in your Watchlist!')
            return redirect('details', movie_id=movie_id)
    return render(request, 'details.html', {'movie': mymovie, 'user': user, 'reviews': reviews_list, 'person': person, 'is_in_watchlist': is_in_watchlist})


def search(request):
    user=request.user
    person = user.username
    if 'q' in request.GET:
        query_string = request.GET.get('q')
        search_results = movies.objects.filter(Q(name__icontains=query_string) | Q(desc__icontains=query_string))
        return render(request, 'search_result.html', {'search_results': search_results,'person':person})
    else:
        return render(request, 'search_result.html', {'search_results': None,'person':person})

def user_logout(request):
    logout(request)
    return redirect('login')

def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('adminindex')
        else:
            messages.error(request,'invalid username or password')
            return render (request,'admin/adminlogin.html')
    return render(request,'admin/adminlogin.html')

def adminindex(request):
    return render(request, 'admin/adminindex.html')

def adminadd(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        year = request.POST.get('year')
        img = request.FILES.get('img')
        user = request.user
        movie = movies(name=name, desc=desc, year=year, img=img, user=user)
        movie.save()
        return redirect('adminadd')
    else:
        pass
    return render(request, 'admin/adminadd.html')

def adminview(request):
    obj = movies.objects.all()
    return render(request,'admin/adminview.html',{'obj':obj}) 

def admindetails(request, movie_id):
    user = request.user
    mymovie = movies.objects.get(id=movie_id)
    person = user.username
    reviews_list = reviews.objects.filter(movie=mymovie).order_by('-id').prefetch_related('replies') 
    return render(request, 'admin/admindetails.html', {'mymovie': mymovie, 'person': person, 'reviews_list': reviews_list, 'movie_id': movie_id})

def update_movies(request, movie_id):
    movie = movies.objects.get(id=movie_id)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('admindetails', movie_id=movie_id)
    else:
        form = UpdateForm(instance=movie)
    return render(request, 'admin/adminupdates.html', {'form': form, 'movie': movie})

def delete(request, movie_id):
    movie = movies.objects.get(id=movie_id)
    movie.delete()
    return redirect('adminview')

@login_required
def review(request, movie_id):
    if request.method == 'POST':
        review_text = request.POST.get('review')
        movie = movies.objects.get(id=movie_id)
        username = request.user.username
        new_review = reviews.objects.create(movie=movie, message=review_text, username=username)
        new_review.save()
        return redirect('details', movie_id=movie_id)
    
def replys(request, movie_id):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review = get_object_or_404(reviews, id=review_id) 
        reply_text = request.POST.get('reply_text')
        username = request.user.username 
        new_reply = reply.objects.create(review=review, message=reply_text, username=username)
        new_reply.save()
        return redirect('admindetails', movie_id=movie_id)
    else:
        return redirect('adminindex')

def viewuser(request):
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'admin/viewuser.html', {'users': users})

def deleteuser(request, user_id):
    currentuser = User.objects.get(id=user_id)
    currentuser.delete()
    return redirect('viewuser')


@login_required
def mywatchlist(request):
    user = request.user
    person = user.username
    watchlist_movies = watchlist.objects.filter(user=user)
    return render(request, 'newwatchlist.html', {'watchlist_movies': watchlist_movies,'person': person})


@login_required
def remove_from_watchlist(request, movie_id):
    user = request.user
    person = user.username
    movie = get_object_or_404(movies, id=movie_id)
    try:
        watchlist_item = watchlist.objects.get(user=user, movie=movie)
        watchlist_item.delete()
        return redirect('newwatchlist') 
    except watchlist.DoesNotExist:
        pass
    return render(request, 'newwatchlist.html', {'person': person})


def viewprofile(request):
    user = request.user
    person = user.username
    email = user.email
    number = watchlist.objects.filter(user=user)
    moviesnumber = number.count()
    return render(request,'viewprofile.html',{'person':person,'email':email,'moviesnumber':moviesnumber})