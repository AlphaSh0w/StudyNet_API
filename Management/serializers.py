from rest_framework import serializers
from .models import Department,Specialty,Section,Assignment

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='teacher_section.section.code')
    class Meta:
        model = Assignment
        exclude = ('teacher_section',)

    def validate(self, attrs):
        #Check that each group in "concerned_groups" exists in the section.
        section = Section.objects.get(code=attrs['teacher_section']['section']['code'])
        for i in attrs['concerned_groups']:
            if i <= 0 or i > section.number_of_groups:
                raise serializers.ValidationError({'concerned_groups':'One of the given groups does not exist.'})

        return attrs