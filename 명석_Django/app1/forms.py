from django import forms
from app1.models import Member, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


'''
# 패스워드 길이 검증
def validate_length(value, min_length=8, max_length=50):
	if (len(str(value)) < min_length) or (len(str(value)) > max_length):
		raise ValidationError(message='패스워드는 최소 8자리 이상, 최대 50자리 이하여야 합니다.'
			, code='Invalid Length')
'''


class UserForm(forms.ModelForm):

	email = forms.EmailField(
		label='Email',
		required=True,
		widget=forms.EmailInput(
			attrs={
				'class': 'register-form',
				'placeholder': '이메일 주소',
				'required': 'True'
			}
		)
	)
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'class': 'register-form',
				'placeholder': '비밀번호',
				'required': 'True'
			}
		),
		label='Password',
		required=True,
		validators=[
			# 패스워드 규칙 검증
			RegexValidator(
				regex=r"^.{8,50}$",
				message="패스워드는 최소 8자리 이상, 최대 50자리 이하여야 합니다.",
				code='Invalid'),

			RegexValidator(
				regex=r"^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#\$%\^&]).*$",
				message="비밀번호는 영문, 숫자조합에 특수문자를 하나 이상 포함하여야 합니다.",
				code='Invalid')
		]
	)
	confirm_password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'class': 'register-form',
				'placeholder': '비밀번호 확인',
				'required': 'True'
			}
		),
		label='Password confirmation'
	)
	nickname = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'class': 'register-form',
				'placeholder': '닉네임',
				'required': 'True'
			}
		),
		validators=[
			# 닉네임 규칙 검증
			RegexValidator(
				regex=r"^[a-zA-Z0-9]{1,20}$",
				message="닉네임은 최대 20자리, 영문과 숫자로만 구성할 수 있습니다.",
				code='Invalid'
			)
		]
	)

	class Meta:
		model = Member
		fields = ('email', 'password', 'confirm_password', 'nickname')

	# 이메일 중복 검사
	def clean_email(self):
		email = self.cleaned_data.get('email')

		if Member.objects.filter(email=email).exists():
			raise ValidationError(
				message="사용중인 이메일입니다.")

		return email

	#패스워드 확인
	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")

		if password != confirm_password:
			raise forms.ValidationError(
				"입력한 비밀번호가 서로 다릅니다."
			)


	# 닉네임 중복 검사
	def clean_nickname(self):
		nickname = self.cleaned_data.get('nickname')
		if Member.objects.filter(nickname=nickname).exists():
			raise ValidationError(
				message="이미 사용중인 닉네임입니다.")

		return nickname

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserForm, self).save(commit=False)
		user.email = UserManager.normalize_email(self.cleaned_data['email'])
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user


