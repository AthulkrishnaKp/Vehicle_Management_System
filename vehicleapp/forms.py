from django import forms
from vehicleapp.models import Vehicle,MyUser
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-primary ","placeholder":"enter password"}))  
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-primary","placeholder":"confirm password"}))              
    
    class Meta:
        model=MyUser
        fields=['username','email','role']

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control border border-primary","placeholder":"enter username"}),
            "email":forms.EmailInput(attrs={"class":"form-control border border-primary","placeholder":"enter email"}),
            "role":forms.Select(attrs={"class":"form-select form-control border border-primary"})
        }        


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border border-info","placeholder":"enter username"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control border border-info","placeholder":"enter password"}))      


class VehicleForm(forms.ModelForm):
    class Meta:
        model=Vehicle
        fields=["vnumber",'vtype','vmodel',"vdescription"]

        widgets={
            "vnumber":forms.TextInput(attrs={"class":"form-control","placeholder":"enter vehicle number"}),
            "vmodel":forms.TextInput(attrs={"class":"form-control","placeholder":"enter vehicle model"}),
            "vdescription":forms.TextInput(attrs={"class":"form-control","placeholder":"enter vehicle description"}),
            "vtype":forms.Select(attrs={"class":"form-select form-control"})
        }    