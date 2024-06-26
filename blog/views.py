from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from blog.models import Blog, Category
from django.db.models import Q
from django.db import models
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here. 

# Lists active and homepage blogs, and paginates them. (Aktif ve ana sayfadaki blogları listeler ve sayfalandırır.)
def index(request):
    blogs_list = Blog.objects.filter(is_active=True, is_home=True)
    paginator = Paginator(blogs_list, 4)  # Show 4 blogs per page

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    context = {
        "blogs": blogs,
        "categories": Category.objects.all()
    }
    return render(request, "blog/index.html", context)

# Displays the details of a blog with the given slug. (Verilen slug'a sahip bir blogun detaylarını görüntüler.)
def details(request, slug):
    blog = Blog.objects.get(slug=slug)
    return render(request, "blog/details.html", {
        "blog": blog,
        "categories": Category.objects.all()
    })

# Returns an empty template page (post.html). (Boş bir şablon sayfa döndürür.)
def post(request):
    return render(request, "blog/post.html")


# Lists active blogs in a specific category. (Belirli bir kategorideki aktif blogları listeler.)
def blogs_by_category(request, slug):
    context = {
        "blogs": Category.objects.get(slug=slug).blog_set.filter(is_active=True),
        "categories": Category.objects.all(),
        "selected_category": slug
    }
    return render(request, "blog/index.html", context)

# Searches blogs by title and description, and lists the results. (Blog başlık ve açıklamalarında arama yaparak sonuçları listeler.)
def search_blogs(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(
            models.Q(title__icontains=query) | models.Q(description__icontains=query)
        )
    else:
        blogs = Blog.objects.none()

    context = {
        "blogs": blogs,
        "categories": Category.objects.all(),
        "query": query
    }
    return render(request, "blog/search_results.html", context)

'''def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BlogForm()
    
    return render(request, 'blog/add_blog.html', {'form': form, 'categories': Category.objects.all()})
'''

# Handles form submission and validation for adding a new blog. Requires user login.
# Yeni bir blog eklemek için form işlemleri ve doğrulama yapar. Kullanıcının giriş yapmasını gerektirir. 
# @login_required
def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('index')
    else:
        form = BlogForm()
    
    return render(request, 'blog/add_blog.html', {'form': form, 'categories': Category.objects.all()})

# Returns the contact page. (İletişim sayfasını görüntüler.)
def contact(request):
    return render(request, 'blog/contact.html', {'categories': Category.objects.all()})