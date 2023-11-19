from django.shortcuts import render ,redirect
from django.http import  JsonResponse,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def home(request):
    context = {}
    all_blogs = blog.objects.all().order_by('-date')
    paginator = Paginator(all_blogs, 2)  # Show 2 blogs per page

    page = request.GET.get('page')
    try:
        all_blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        all_blogs = paginator.page(paginator.num_pages)

    if request.POST:
        query = request.POST.get('query')
        all_blogs = blog.objects.filter(Q(title__contains=query) | Q(user__user__username__contains=query))

    if request.user.is_authenticated:
        context['bloger'] = user_profile.objects.filter(user=request.user).first()

    context['all_blogs'] = all_blogs
    context['all_categories'] = blog_category.objects.all()
    return render(request, 'home.html', context)

   

def add_subscription(request):
    if request.POST:
        getPlan = subcription.objects.get(id=request.POST.get("subscription"))
        user_profile.objects.filter(user=request.user).update(subscription=getPlan)
        messages.success(request , "Subscription Added Successfully")
        return redirect('home')
    
    getPlans = subcription.objects.all()
    return render(request ,'plan.html' , locals())
    
        

def filter_by_category(request,id):
    context={}
    all_blogs   = blog.objects.filter(category__id=id)
    if request.user.is_authenticated:
        context['bloger'] =  user_profile.objects.filter(user=request.user).first()

    context['all_blogs']=all_blogs
    context['all_categories']=blog_category.objects.all()
    return render(request, 'home.html', context)
   


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save user information
            user = form.save()
            # Save candidate information
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            user_profile.objects.create(user=user, name=name, email=email, phone=phone)
            messages.success(request , "You account created Successfully ")
            return redirect('user-login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('home')
        else:
            messages.success(request, 'Please Enter valid credentials')
            return redirect('user-login')
    else:
        return render(request, 'login.html')


def log_out(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')



def blog_view(request , pk):
    context={}
    get_blog=blog.objects.filter(id=pk).first()
    
    if request.user.is_authenticated:
        context['bloger'] =  user_profile.objects.filter(user=request.user).first()
    
    context['post'] = get_blog 

   
    return render(request , 'blog_view.html' , context)



def add_blog(request):
    check_Plan = user_profile.objects.get(user=request.user)
    if check_Plan.subscription:
        form = AddBlog()
        get_user=user_profile.objects.filter(user=request.user).first()
        if request.method == 'POST':
            if blog.objects.filter(user=check_Plan).count() >= check_Plan.subscription.post_limit :
                messages.success(request, 'Your post limit is over plaese purchase another plan')
                return redirect('home') 
            
            form = AddBlog(request.POST)
            if form.is_valid():
                fr=form.save(commit=False)
                fr.user = get_user
                fr.save()
                messages.success(request, 'Blog added Successfully')
                return redirect('home')
        return render(request, 'blog.html', {'form': form , 'bloger':user_profile.objects.filter(user=request.user).first()})
    else:
        messages.success(request, 'You have No Active Subscription ')
        return redirect('home')


def update_blog(request,pk):
    check_Plan = user_profile.objects.get(user=request.user).subscription
    if check_Plan:
        blog_obj = blog.objects.get(pk=pk)
        form = AddBlog(instance=blog_obj)
        if request.method == 'POST':
            form = AddBlog(request.POST , instance=blog_obj)
            if form.is_valid():
                form.save()
                return redirect('profile')
        return render(request, 'blog.html', {'form': form , 'bloger':user_profile.objects.filter(user=request.user).first()})   
    else:
        messages.success(request, 'You have No Active Subscription ')
        return redirect('home')
     

def delete_blog(request,pk):
    check_Plan = user_profile.objects.get(user=request.user).subscription
    if check_Plan:
        blog_obj = blog.objects.get(pk=pk)
        blog_obj.delete()
        messages.success(request, 'deleted successfully')
        return redirect('profile')
    else:
        messages.success(request, 'You have No Active Subscription ')
        return redirect('home')

def profile(request):
    get_user = user_profile.objects.get(user=request.user)
    all_blogs= blog.objects.filter(user=get_user)
    return render(request, 'profile.html', {'all_blogs': all_blogs , 'bloger':get_user})    



class UserProfileUpdateView(UpdateView):
    model = user_profile
    form_class = UserProfileForm
    template_name = 'update_profile.html'  
    success_url = reverse_lazy('profile')  




