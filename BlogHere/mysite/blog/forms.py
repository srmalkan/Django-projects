from django import forms
from .models import Comment,post


class EmailForm(forms.Form):
    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control'}))
    to = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control'}))
    comments = forms.CharField(required=False,widget = forms.Textarea(attrs={'class':'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name","email","body",)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
        }

class addPostForm(forms.ModelForm):
    
    class Meta:
        model = post
        fields = ("title","body","tags")
        widgets = {
            'title': forms.TextInput(attrs ={'class':'form-control'}),
            'body':forms.Textarea(attrs ={'class':"form-control"}),
            'tags':forms.TextInput(attrs ={'class':'form-control'}),
        }

class updateForm(forms.Form):
    title = forms.CharField(max_length=250,widget =forms.TextInput(attrs={'class':"form-control"}))
    body = forms.CharField(widget =forms.Textarea(attrs={'class':"form-control"}))
    tags = forms.CharField(widget =forms.TextInput(attrs={'class':"form-control"}))
