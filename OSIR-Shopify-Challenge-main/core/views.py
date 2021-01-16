from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from core.models import ImageItem, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ImageForm, UserRegistrationForm



# Helper Functions
def not_logged_in(user):
    return not user.is_authenticated

# View Functions
def home(request):
    return render(request, "core/index.html")

@user_passes_test(not_logged_in,'/')
def login_view(request):
    context = {"error": None}
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context["error"] = "Could not login"
    return render(request, "core/login.html", context)

@user_passes_test(not_logged_in,'/')
def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(email=email,password=password)
            user.save()
            user = authenticate(request, username=email, password=password)
            login(request, user)
            return redirect('/')
        else:
            raise Http404(form.errors)
    return render(request, "core/signup.html")

def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            model = ImageItem(**form.cleaned_data, uploaded_by=request.user)
            model.save()
            return redirect('/')
    else:
        form = ImageForm()

    return render(request, 'core/upload.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def delete_image(request, id):
    obj = get_object_or_404(ImageItem, id = id)
    if obj.uploaded_by == request.user:
        obj.delete()
        return redirect('/images')
    else:
        raise Http404()

class ImageListView(ListView):
    model = ImageItem
    template_name ="core/images.html"
    queryset = ImageItem.objects.filter(public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['private_images'] = ImageItem.objects.filter(public=False, uploaded_by=self.request.user)
        return context