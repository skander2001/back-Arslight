from rest_framework import serializers
from .models import Student, Parent, Teacher, User, Orthophoniste


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_student', 'is_parent', 'is_teacher', 'gender', 'phone']

    def create(self, validated_data):
        return super().create(validated_data)


class StudentSerializer(serializers.ModelSerializer):
    student = UserSerializer()  # Use separate serializer for writing data

    class Meta:
        model = Student
        fields = ['student', 'level', 'child_first_name', 'child_last_name']

    def create(self, validated_data):
        user_data = validated_data.pop('student')
        user = User.objects.create(**user_data)
        student = Student.objects.create(student=user, **validated_data)
        return student


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer for the 'user' field

    class Meta:
        model = Parent
        fields = ['first_name', 'last_name', 'user']  # Include 'user' field

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)  # Create the User object
        user.is_parent = True  # Set the user role to 'parent'
        user.save()
        parent = Parent.objects.create(user=user, **validated_data)  # Create the Parent object
        return parent


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher




class OrthoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user.is_orthophoniste = True
        user.save()
        ortho = Orthophoniste.objects.create(user=user, **validated_data)
        return ortho