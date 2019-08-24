from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone


class UserManager(BaseUserManager):
	def create_user(self, email, password, nickname):
		if not email:
			raise ValueError("사용할 이메일을 입력하세요")

		user = self.model(
			# 이메일의 domain 부분은 case-insensitive이므로,
			# normalize_email()을 써서 domain 부분을 소문자로 변환함
			email=self.normalize_email(email),
			nickname=nickname
		)

		user.set_password(password)  # create a hashed password
		user.save()
		return user

	def create_superuser(self, email, password, nickname):
		user = self.create_user(
			email=email,
			password=password,
			nickname=nickname,
		)

		user.is_superuser = True  # superuser 권한 주기
		user.save()
		return user


# Create your models here.
class Member(AbstractBaseUser, PermissionsMixin):
	user = models.AutoField(  # User 고유번호
		primary_key=True,
		unique=True,
		blank=False
	)
	email = models.CharField(  # 이메일
		max_length=50,
		unique=True,
		blank=False
	)
	password = models.CharField(  # 비밀번호
		max_length=255,
		blank=False
	)
	nickname = models.CharField(  # 닉네임
		max_length=30,
		blank=False
	)
	date_joined = models.DateTimeField(  # 가입 날짜
		default=timezone.now
	)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['password', 'nickname']

	class Meta:
		verbose_name = 'user'  # 모델명
		verbose_name_plural = 'users'  # 모델명(복수형)
		ordering = ('-date_joined',)  # 컬럼 순서 설정

	@property
	def is_staff(self):
		return self.is_superuser
