from rest_framework import serializers
from .models import Student, Parent, Teacher, User, Orthophoniste


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'is_student', 'is_parent', 'is_teacher', 'gender', 'phone']

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
        student_data = validated_data.pop('student', None)  # Get student data if available
        user = User.objects.create_user(**user_data)  # Create the User object
        user.is_parent = True  # Set the user role to 'parent'
        user.save()
        parent = Parent.objects.create(user=user, **validated_data)

        # Check if student data is provided and create the student
        if student_data:
            student_user_data = student_data.pop('user')
            student_user = User.objects.create_user(**student_user_data)  # Create the student User object
            student_user.is_student = True  # Set the user role to 'student'
            student_user.save()
            student = Student.objects.create(student=student_user, **student_data)  # Create the Student object
            parent.student = student  # Associate the student with the parent
            parent.save()

        return parent



class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Use UserSerializer to handle user information

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Extract user data from validated data
        user = User.objects.create_user(**user_data)  # Create a user object using the extracted user data
        user.is_teacher = True  # Set the user role to teacher
        user.save()
        teacher = Teacher.objects.create(user=user, **validated_data)  # Create the teacher object
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