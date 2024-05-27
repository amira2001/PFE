from django.contrib import admin
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
from .forms import SuperuserLoginForm



urlpatterns = [
    path('Dashboard',views.Dashboard,name="Dashboard"),
    path('analyseChurn',views.analyseChurn,name="analyseChurn"),
    #path('livre',views.ADD_LIVRE,name="add_get_all_livres"),
    #path('livre/<int:id>/',views.LIVRE_CRUD,name="delete_get"),
    #path('livre/<int:id_livre>/<int:id_user>/',views.EMPREINT,name="empreinter")
    path('', auth_views.LoginView.as_view(authentication_form=SuperuserLoginForm), name='login'),
    path('logout/', views.user_logout, name='logout'),

]