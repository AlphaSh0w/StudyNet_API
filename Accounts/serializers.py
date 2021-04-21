from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from Management.models import Section,TeacherSection
from .models import User,Student,Teacher


class CreateUserSerializer(serializers.ModelSerializer):
    """
        Used to display and create a user.
    """
    class Meta:
        model = User
        fields = ['id','password','email','first_name','last_name','user_type','last_login','date_joined']
        read_only_fields = ('user_type','last_login','date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

class CreateStudentSerializer(serializers.ModelSerializer):
    """
        Used to display and create a student.
    """
    user = CreateUserSerializer(many=False)
    class Meta:
        model = Student
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        #Create the user
        user = User.objects.create_user(**user_data,user_type=User.Types.STUDENT)
        #Create the student account and assign to it the created user
        return Student.objects.create(**validated_data,user=user)

class TeacherSerializer(serializers.ModelSerializer):
    """
        Only used to display a teacher.
    """
    user = CreateUserSerializer(many=False)
    class Meta:
        model = Teacher
        fields = '__all__'

class SectionCharField(serializers.CharField):
    """
        An overriden serializer charfield with a custom validation.
        This charfield expects a section code then checks if that section exists.
    """
    def run_validation(self, data=serializers.empty):
        value = super().run_validation(data)
        #Check that the given section exists.
        if not Section.objects.filter(code=value).exists():
            raise ValidationError('section \"' + value + '\" does not exist.')
        return value

class CreateTeacherSerializer(serializers.ModelSerializer):
    """
        Only used to create a teacher with optionally their assigned sections.
    """
    user = CreateUserSerializer(many=False,required=True)
    sections = serializers.ListField(child=SectionCharField(),required=False)
    
    class Meta:
        model = Teacher
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        sections = validated_data.pop('sections',[])

        #Create the user.
        user = User.objects.create_user(**user_data,user_type=User.Types.TEACHER)
        #Create the teacher account and assign to it the created user.
        teacher = Teacher.objects.create(**validated_data,user=user)
        #Assign to the teacher the given sections.
        for section in sections:
            section = Section.objects.get(code=section)
            TeacherSection.objects.create(teacher=teacher,section=section)
        return teacher