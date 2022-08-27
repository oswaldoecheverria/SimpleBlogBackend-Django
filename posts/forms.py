
from dataclasses import fields
from .models import PostModel, CommentModel
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ('__all__')

# Logica del comentario
"""
Creamos el form solo con el contenido por que 
los otros campos se los integra de otra forma 

"""

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('content',)

