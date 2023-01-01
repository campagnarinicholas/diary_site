from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'diary_app' # Add namespace to URLcof
urlpatterns = [
    #path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('create_entry_type/', 
        login_required(views.EntryTypeCreateView.as_view(), login_url='diary_app:signin'),
        name='create_entry_type'),
    path('<int:pk>/entry_type/', 
        login_required(views.entry_type_entry_list, login_url='diary_app:signin'), 
        name='entry_type'),
    path('', 
        login_required(views.EntryChartView.as_view(), login_url='diary_app:signin'), 
        name='home'),
    path('create_entry/',
        login_required(views.EntryCreateView.as_view(), login_url='diary_app:signin'),
        name='create_entry'),
    path('create_entry/<int:pk>',
        login_required(views.EntryCreateView.as_view(), login_url='diary_app:signin'),
        name='create_typed_entry'),
    path('<int:pk>/delete_entry/',
        views.delete_entry,
        name='delete_entry'),    
    path('entry_list/',
        login_required(views.entry_list, login_url="../signin"),
        name="entry_list")
]