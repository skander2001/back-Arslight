from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.urls import reverse
from django.db.models import Q
from rest_framework.authtoken.models import Token
from .validators import ASCIIUsernameValidator

GENDERS = (("M", "Male"), ("F", "Female"))
LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    ("1ere année", "1ere année"),
    ("2eme année", "2eme année"),
    ("3eme année", "3eme année"),
)

class CustomUserManager(UserManager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset

    def get_student_count(self):
        return self.model.objects.filter(is_student=True).count()

    def get_teacher_count(self):
        return self.model.objects.filter(is_teacher=True).count()

    def get_parent_count(self):
        return self.model.objects.filter(is_parent=True).count()




class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True,blank=False,null=False)
    is_student = models.BooleanField(default=False,blank=True,null=True)
    is_parent = models.BooleanField(default=False,blank=True,null=True)
    is_orthophoniste= models.BooleanField(default=False,blank=True,null=True)
    is_teacher = models.BooleanField(default=False,blank=True,null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=False, null=False)
    phone = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=100,blank=False,null=False)

    username_validator = ASCIIUsernameValidator()
    objects = UserManager()

    def __str__(self):
        return "{} ({})".format(self.username, self.get_full_name())

    @property
    def get_user_role(self):
        if self.is_orthophoniste:
            role = "Orthophoniste"
        elif self.is_student:
            role = "Student"
        elif self.is_teacher:
            role = "Teacher"
        elif self.is_parent:
            role = "Parent"
        return role

class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = Q(level__icontains=query)
            qs = qs.filter(
                or_lookup
            ).distinct()
        return qs


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    child_first_name = models.CharField(max_length=120)
    child_last_name = models.CharField(max_length=120)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)

    objects = StudentManager()

    class Meta:
        ordering = ("-student__date_joined",)

    def __str__(self):
        return self.student.get_full_name


    @classmethod
    def get_gender_count(cls):
        males_count = Student.objects.filter(student__gender="M").count()
        females_count = Student.objects.filter(student__gender="F").count()

        return {"M": males_count, "F": females_count}

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    def delete(self, *args, **kwargs):
        self.student.delete()
        super().delete(*args, **kwargs)

class Parent(models.Model):
    """
    Connect student with their parent, parents can
    only view their connected students information
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    #department = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return "{}".format(self.user)


class Orthophoniste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return "{}".format(self.user)


