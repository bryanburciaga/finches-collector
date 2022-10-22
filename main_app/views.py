from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth import login

from .forms  import FeedingForm
from django.contrib.auth.forms import UserCreationForm

from .models import Finch

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', {'finches': finches})

@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch, 
        'feeding_form': feeding_form
    })

@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST) 
    
    if form.is_valid():
      new_feeding = form.save(commit=False) 
      new_feeding.finch_id = finch_id
      new_feeding.save()
    else: 
        print(form.errors)
    return redirect('finches_detail', finch_id=finch_id)


def signup(request):
    # POST Request
    error_message = None
    if request.method == 'POST':
        # Capture user input from a form
        form = UserCreationForm(request.POST)
        # checl the form to ensure it's a valiD
        if form.is_valid():
            # use the user input to create a new user in the database
            user = form.save()
            # log the user in
            login(request, user)
            # redirect the user to the cats_index page
            return redirect('finches_index')
        else:
            error_message = 'Signup input invalid - Please try again'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form })

class FinchesCreate(CreateView):
    model = Finch
    fields = ('name', 'breed', 'description', 'age')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FinchesUpdate(UpdateView):
    model = Finch
    fields = ('age', 'description')

class FinchesDelete(DeleteView):
    model = Finch
    success_url = '/finches/'