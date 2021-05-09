from rest_framework import serializers
from .models import Department,Specialty,Section,Assignment,Module,ModuleSection

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

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='teacher_section.section.code')
    module = serializers.CharField(source='module_section.module.code')
    class Meta:
        model = Assignment
        exclude = ('teacher_section','module_section')

    def validate(self, attrs):
        section_code = attrs['teacher_section']['section']['code']
        module_code = attrs['module_section']['module']['code']
        if Section.objects.filter(code=section_code).exists():
            #Check that each group in "concerned_groups" exists in the section.
            section = Section.objects.get(code=section_code)
            for i in attrs['concerned_groups']:
                if i <= 0 or i > section.number_of_groups:
                    raise serializers.ValidationError({'concerned_groups':'One of the given groups does not exist.'})
        #Check that the given module does exist.
        if not Module.objects.filter(code=module_code).exists():
            raise serializers.ValidationError({'module':'Module does not exist.'})
        #Check that the given module type is supported by the module
        if not attrs['module_type'] in Module.objects.get(code=module_code).types:
            raise serializers.ValidationError({'module_type':'The module ' + module_code + ' does not have teaching of type ' + attrs['module_type']})
        #Check that the given module is assigned to the section.
        if not ModuleSection.objects.filter(section=section_code,module=module_code).exists():
            raise serializers.ValidationError({'module':'The module ' + module_code + ' is not assigned to the section ' + section_code})
        return attrs