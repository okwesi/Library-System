from audioop import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import  ListView

from requests import request
from books.forms import BookForm
from django.urls import reverse
from django.contrib import messages

from books.models import Book, Category, NewBooks
from library_app.models import Library
from request.forms import SchoolRequestForm

# Create your views here.
# def add_book():
#     pass
# For admin 
class LibrarianBookListView(ListView):
    model = Book
    template_name = 'librarian/books.html'
    context_object_name = "books"
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        # context["library"] = self.request.
        return context


def add_book(request): 
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        form.fields["category"].queryset = Category.objects.filter(library=request.user.librarian.library)

        if form.is_valid():
            print("Form is valid")
            category = form.cleaned_data["category"]
            title = form.cleaned_data["title"]
            stock = form.cleaned_data["stock"]
            book_cover = request.FILES["book_cover"]
            about = form.cleaned_data["about"]

            book = Book.objects.create(title=title, about=about, book_cover=book_cover,
             stock=stock, library=request.user.librarian.library, category=category)
            messages.info(request, f'{title} has been added')
            return redirect("get-books")
        print(form.errors)
    form = BookForm()
    form.fields["category"].queryset = Category.objects.all()

    # category = Category.objects.filter(library=request.user.librarian.library_id)
    return render(request, 'librarian/add_book.html', {"form":form,})
        

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        form.fields["category"].queryset = Category.objects.filter(library=request.user.librarian.library)

        if form.is_valid(): 
            form.save()
            messages.success(request, f'{book.title} has been updated')
            return redirect("get-books")
        print(form.errors)
    form = BookForm(instance=book)
    form.fields["category"].queryset = Category.objects.filter(library=request.user.librarian.library)

    messages.error(request, form.errors)
    return render(request, 'librarian/edit_book.html', {"form":form, "book":book,})
    

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    title = book.title
    book.delete()
    messages.warning(request, f'{title} has been deleted')
    return redirect("get-books")


#for schools and students
class BookListView(ListView):
    model = Book
    template_name = 'books/bookshelf.html'
    context_object_name = "books"
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            if self.request.user.groups.filter(name='student').exists():
                object_list = self.model.objects.filter(library=self.request.user.student.school.library)
            elif self.request.user.groups.filter(name='school').exists():
                object_list = self.model.objects.filter(library=self.request.user.school.library)
            # else:
            #     object_list = self.model.objects.filter(library=self.request.user.librarian.library)

            elif self.request.user.groups.filter(name='librarian').exists():
                object_list = self.model.objects.all(library=self.request.user.librarian.library)
            elif self.request.user.groups.filter(name='super Librarian').exists():
                object_list = self.model.objects.filter(library=self.request.user.librarian.library)
            else:
                object_list = self.model.objects.all()

        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='student').exists():
            context["library"]=self.request.user.student.school.library.id
        elif self.request.user.groups.filter(name='school').exists():
            context["library"]=self.request.user.school.library.id
        elif self.request.user.groups.filter(name='librarian').exists():
            context["library"]=self.request.user.librarian.library.id
        elif self.request.user.groups.filter(name='super Librarian').exists():
            context["library"]=self.request.user.librarian.library.id
                
        return context


# get the details of the books
def book_detail(request, id):
    book = Book.objects.get(id=id)
    if request.user.groups.filter(name="student").exists():
        borrowed = request.user.student.borrowed
    elif request.user.groups.filter(name="school").exists():
        borrowed = request.user.school.borrowed
    else:
        borrowed = False
    request_form = SchoolRequestForm()   
 
    context = {
        "book" : book,
        "borrowed" : borrowed,
        "request_form" : request_form
    }
    return render(request, "books/book_detail.html", context)



def public_get_libraries(request):
    libraries = Library.objects.all()
    return render(request, "books/libraries.html", {"libraries" : libraries })


def get_public_books(request, library_id):
    books = Book.objects.filter(library = library_id)
    if request.method == "GET":
        title = request.GET.get("search")
        books = books.filter(title__icontains=title)
        return render(request, 'books/bookshelf.html', {'books': books})
    else:
        return render(request, 'books/bookshelf.html', {'books': books})


class PublicBookListView(ListView):
    model = Book
    template_name = 'books/bookshelf.html'
    context_object_name = "books"
    paginate_by = 20
    
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('search')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.model.objects.filter(library_id=self.kwargs['library_id'])
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["library"] = self.kwargs['library_id']
        return context



def add_category(request):

    if request.method == "POST":
        name = request.POST.get("name")
        library = request.user.librarian.library
        category = Category.objects.create(name=name, library=library)
        messages.success(request, f'New Category added')
        return redirect("get-books")


def add_new_book(request, library_id):
    if request.method == "POST":
        name = request.POST.get("name")
        library=get_object_or_404(Library, id=library_id)
        new_book = NewBooks.objects.create(name=name, library=library)
        messages.success(request, "Request has been accepted😊", extra_tags='alert alert-success alert-dismissible fade show')
        if request.user.is_authenticated:
            return redirect('public-books')
        else:
            return HttpResponseRedirect(reverse('get_public_books', kwargs={'library_id': library.id}))

            # return HttpResponseRedirect(reverse('get_public_books', kwargs={'library_id':library_id}))

    else:
        messages.error(request, "Something Went Wrong, Please fill the forms again")
        return HttpResponseRedirect(reverse('get-books'))























def get_books(request):
    print(request.user.library.id)
    books = Book.objects.filter(library=request.user.librarian.library)    
    return render(request, 'librarian/books.html', {'books':books})

# def add_book(request):
#     """functions for adding books to database"""
#     bookForm = BookForm()
#     # request.is_ajax() and 
#     if request.method == "POST":
#         bookForm = BookForm(request.POST or None)
#         if bookForm.is_valid():
            
#             print(bookForm.cleaned_data.get("title"))
#             print(bookForm.cleaned_data.get("about"))
#             print(str(request.user.librarian.library.name))
#             print(bookForm.cleaned_data.get("stock"))
                      
#             #save form in database
#             book = bookForm.save(commit=False)
#             book.library = request.user.librarian.library
#             book.save() 
            
#             print(book.id)
                     
#             return JsonResponse({
#                 'book_id' : book.id,
#                 'title': bookForm.cleaned_data.get("title"),
#                 'about' : bookForm.cleaned_data.get("about"),
#                 'library' : str(request.user.librarian.library.name),
#                 'stock' : bookForm.cleaned_data.get("stock"),
#             })
#         print("after", book.id)
#     context = {
#         "bookForm" : bookForm
#     }    
#     return render(request, "library/super_dashboard.html", context)



class BookAddView(CreateView):
    """used to create form and post a blog with the same class"""
    model = Book
    form_class = BookForm
    # fields = "__all__"
    success_url = reverse_lazy('home')
    template_name="library/super_dashboard.html"

    
    # def form_valid(self, form):
    #     form.instance.library = self.request.user.librarian.library
    #     return super().form_valid(form)
    

# def update_book(request, pk):
#     object = Book.objects.get(id=pk)
    
#     update_form = BookForm(instance=object)
    
#     return render(request, 'library/editbook.html', {"update_form": update_form})




# def book_detail(request, id):
#     book = Book.objects.get(id=id)
#     update_form = BookForm(instance=book)
    
#     context = {
#         "book" : book,
#         "update_form" : update_form
#     }
#     return render(request, "library/book_detail.html", context)


def  update_book(request, id):

    context ={} 
    book = get_object_or_404(Book, id=id) 
    form = BookForm(request.POST or None, instance = book)
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('book-detail', args=[str(id),]))

    context["update_form"] = form
 
    return render(request, "library/book_detail.html", context)



# def delete_book(request, id):
#     book = Book.objects.get(id=id)
#     if request.method == "POST":
#         book.delete()
#     return redirect('library_admin')