from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,ListView,UpdateView,View
from vehicleapp.forms import RegistrationForm,LoginForm,VehicleForm
from django.urls import reverse_lazy
from vehicleapp.models import MyUser,Vehicle
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


# Create your views here.


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)    
    return wrapper

def superadmin_required(user):
    return user.is_authenticated and user.role in (1)

def admin_or_superadmin_required(user):
    return user.is_authenticated and user.role in (1,2)

decs=[never_cache,signin_required,user_passes_test(admin_or_superadmin_required)]
aces=[never_cache,signin_required,user_passes_test(superadmin_required)]
cdes=[signin_required,never_cache]


class SignupView(CreateView):
    model=MyUser
    form_class=RegistrationForm
    template_name='register.html'
    success_url=reverse_lazy('signin')

class LoginFormView(FormView):
    form_class=LoginForm
    template_name='login.html'

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)   
        if form.is_valid():
            uname=form.cleaned_data.get("username")   
            pwd=form.cleaned_data.get("password") 
            usr=authenticate(request,username=uname,password=pwd) 
            if usr:
                login(request,usr)
                return redirect('home')
            else:                            
                return render(request,"login.html",{"form":form})    

@method_decorator(cdes,name="dispatch")
class HomeView(CreateView,ListView):            
    model=Vehicle
    form_class=VehicleForm
    template_name='home.html'
    context_object_name="vehicle"
    success_url=reverse_lazy("home")
    pk_url_kwarg='id'

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        vehicle=Vehicle.objects.all()
        context['vehicle']=vehicle
        user=MyUser.objects.all()
        context['user']=user
        return context

@method_decorator(decs,name="dispatch")   
class VehicleUpdateView(UpdateView):
    model=Vehicle
    form_class=VehicleForm
    template_name="vupdate.html"
    pk_url_kwarg='id'
    success_url=reverse_lazy("home")    

@method_decorator(aces,name="dispatch")
class VehicleDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Vehicle.objects.filter(id=id).delete()     
        return redirect("home")    
    

def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")    