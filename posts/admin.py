from django.contrib import admin
from .models import PostModel, PostViewtModel, LikeModel, CommentModel, UserModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(PostModel)
admin.site.register(PostViewtModel)
admin.site.register(LikeModel)
admin.site.register(CommentModel)