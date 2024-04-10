from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'news', views.NewsViewset)
router.register(r'comments', views.CommentsViewset)

urlpatterns = router.urls

urlpatterns += [
    path("token", obtain_auth_token),
    path('register', views.RegisterView.as_view()),
    path('user', views.UserViewset.as_view()),
    path('news/<pk>/bookmark/', views.BookmarkViewset.as_view()),
]