# dappx/urls.py
from django.conf.urls import url
from django.urls import path
from app1 import views


# SET THE NAMESPACE!
app_name = 'app1'

urlpatterns=[
	path('register/', views.register, name='register'),			# 회원가입
	path('user_login/', views.user_login, name='user_login'),	# 로그인
	path('logout/', views.user_logout, name='user_logout'),		# 로그아웃
]