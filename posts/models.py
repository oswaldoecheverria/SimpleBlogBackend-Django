from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse

# Create your models here.

class UserModel(AbstractUser):
    pass

    def __str__(self):
        return self.username

class PostModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # Miniatura del post
    thumbnail = models.ImageField()
    publish_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

    # ESta funcion es despues de crear la funcion de dar like y dislike en el view
    def get_like_url(self):
        return reverse("like", kwargs={"slug": self.slug})

    #Funcion propiedad para contar los comentarios, likes y vistas  
    @property
    def get_comment_count(self):
        return self.commentmodel_set.all().count()

    @property
    def get_like_count(self):
        return self.likemodel_set.all().count()

    @property
    def get_view_count(self):
        return self.postviewtmodel_set.all().count()

    # Con esta propiedad podemos acceder a los comentarios 
    @property
    def comments(self):
        return self.commentmodel_set.all()
    

class CommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    # hace que tiempo fue creado el comentario 
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username


# Cuantas veces alguien ha visto el post 
# Nota: tiene un t de mas el nombre del modelo
class PostViewtModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    # hace que tiempo fue creado el comentario 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# Modelo para Likes
class LikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username