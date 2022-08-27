from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import PostModel, PostViewtModel, LikeModel, CommentModel, UserModel
from .forms import PostForm, CommentForm

# Create your views here.
class PostListView(ListView):
    model = PostModel
    template_name = 'posts/post_list.html'


class PostDetailView(DetailView):
    model = PostModel
    template_name = 'posts/post_detail.html'

    

    #Logica de los comentarios 
    def post(self, *args, **kwargs):
        #Definimos primero el formulario que sera para el post 
        form = CommentForm(self.request.POST)
        # Si el formulario es valido 
        if form.is_valid():
            #Obtenemos el objeto del post 
            post = self.get_object()
            #Obtenemos una instancia del formulario el cual llamamos comment
            comment = form.instance
            # Otenemos una instancia del usuario que hizo el post 
            comment.user = self.request.user
            # Y el mismo post de la instancia del comentario 
            comment.post = post
            # Guardamos el comentario
            comment.save()
            return redirect("detail", slug=post.slug)
        #En caso que el comentario sea vacio 
        return redirect("detail", slug=self.get_object().slug)

    #Logica de las vistas de post 
    #El get_object permite agrarrar el objeto del postmodel
    def get_object(self, **kwargs):
        #Lo definimos 
        object = super().get_object(**kwargs)
        if self.request.user.is_authenticated:
            #La logica  para usuarios logeados que ven un post
            PostViewtModel.objects.get_or_create(user=self.request.user, post=object)
        return object

    # Pasamos el contexto del comentario 
    def get_context_data(self, **kwargs):
        # Definimos el contexto y traemos lo kwarg arguments
        context = super().get_context_data(**kwargs)
        # Le decimos que actualice en forma de diccionario
        context.update({
            'form': CommentForm()
        })
        return context



class PostCreateView(CreateView):
    form_class = PostForm
    model = PostModel
    template_name = 'posts/post_create.html'
    

    def get_context_data(self, **kwargs):
        """
        Esta configuracion view_type nos permite guardar en esa variable 
        el nombre del modelo para que lo podamos referenciar en html
        
        """
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context
    

class PostUpdateView(UpdateView):
    form_class = PostForm
    model = PostModel
    template_name = 'posts/post_form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context
    

class PostDeleteView(DeleteView):
    model = PostModel
    success_url = '/'



#Implementamos una funcion para la logica de los likes
def like(request, slug):
    post = get_object_or_404(PostModel, slug=slug)
    like_query_set = LikeModel.objects.filter(user=request.user, post=post)

    if like_query_set.exists():
        like_query_set[0].delete()
        return redirect('detail', slug=slug)
    LikeModel.objects.create(user=request.user, post=post)
    return redirect('detail', slug=slug)

    # Esta funcion la registramos en url.py con las demas vistas 
    #y creamos un path con la funcion