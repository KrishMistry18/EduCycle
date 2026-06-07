from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Item
import re

class UserRegistrationForm(forms.ModelForm):
    # Enhanced password field with validation
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'password1'
        }),
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")]
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'password2'
        })
    )
    
    # Enhanced user fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'id': 'first_name'
        }),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message="First name can only contain letters and spaces."
            )
        ]
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
            'id': 'last_name'
        }),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message="Last name can only contain letters and spaces."
            )
        ]
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a unique username',
            'id': 'username'
        }),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message="Username can only contain letters, numbers, and underscores."
            ),
            MinLengthValidator(3, message="Username must be at least 3 characters long.")
        ]
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'id': 'email'
        })
    )
    
    # Student-specific fields
    student_id = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your student ID',
            'id': 'student_id'
        }),
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9]+$',
                message="Student ID can only contain uppercase letters and numbers."
            )
        ]
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number (optional)',
            'id': 'phone_number'
        }),
        validators=[
            RegexValidator(
                regex=r'^[\+]?[1-9][\d]{0,15}$',
                message="Please enter a valid phone number."
            )
        ]
    )
    
    department = forms.ChoiceField(
        choices=[
            ('', 'Select your department'),
            ('computer_science', 'Computer Science'),
            ('engineering', 'Engineering'),
            ('arts', 'Arts & Design'),
            ('business', 'Business'),
            ('science', 'Science'),
            ('medicine', 'Medicine'),
            ('law', 'Law'),
            ('education', 'Education'),
            ('other', 'Other')
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'department'
        })
    )
    
    year_of_study = forms.ChoiceField(
        choices=[
            ('', 'Select your year'),
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
            ('5', '5th Year'),
            ('graduate', 'Graduate'),
            ('phd', 'PhD')
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'year_of_study'
        })
    )
    
    # Terms and conditions
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'terms_accepted'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            # Check password strength
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            
            if not re.search(r'[A-Z]', password1):
                raise forms.ValidationError("Password must contain at least one uppercase letter.")
            
            if not re.search(r'[a-z]', password1):
                raise forms.ValidationError("Password must contain at least one lowercase letter.")
            
            if not re.search(r'\d', password1):
                raise forms.ValidationError("Password must contain at least one number.")
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
                raise forms.ValidationError("Password must contain at least one special character.")
        
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if student_id and UserProfile.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This student ID is already registered.")
        return student_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                phone_number=self.cleaned_data.get('phone_number', ''),
                department=self.cleaned_data['department'],
                year_of_study=self.cleaned_data['year_of_study']
            )
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email',
            'id': 'username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'password'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'remember_me'
        })
    )

class ItemForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter item name'
        }),
        validators=[
            MinLengthValidator(3, message="Item name must be at least 3 characters long.")
        ]
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe your item in detail...'
        }),
        validators=[
            MinLengthValidator(10, message="Description must be at least 10 characters long.")
        ]
    )
    
    price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter price (leave empty if free)',
            'min': '0',
            'step': '0.01'
        })
    )
    

    
    image1 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    image2 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'price', 'image1', 'image2']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_image1(self):
        image = self.cleaned_data.get('image1')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file size must be less than 5MB.")
        return image

    def clean_image2(self):
        image = self.cleaned_data.get('image2')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file size must be less than 5MB.")
        return image 