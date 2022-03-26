from django.urls import path, include
from . import views
from rest_framework import routers
from django.contrib.auth.views import LoginView, LogoutView

router = routers.DefaultRouter()
router.register('myapi', views.approvalView)
urlpatterns = [
    path('', views.index, name='index2'),
    path('calc/', views.cxcontact, name='cxform'),
    path('api/', include(router.urls)),
    path('calc/calculator/', views.calculator, name='calculator'),
    path('calc/signup/', views.signup, name='signup'),
    path('calc/login/', LoginView.as_view(template_name='myform/login.html'), name='login'),    
    path('calc/logout/', LogoutView.as_view(next_page='index2'), name='logout'),
]