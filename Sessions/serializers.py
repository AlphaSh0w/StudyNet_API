from rest_framework import serializers
from django.db.models import Q
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    teacher_email = serializers.SerializerMethodField()
    module = serializers.SerializerMethodField()
    module_type = serializers.SerializerMethodField()

    read_only_fields = ('teacher_name','teacher_email','module','module_type')
    class Meta:
        model = Session
        fields = '__all__'
    
    def get_teacher_name(self, instance):
        return instance.assignment.teacher_section.teacher.user.first_name[0]+'. '+ instance.assignment.teacher_section.teacher.user.last_name
    def get_teacher_email(self, instance):
        return instance.assignment.teacher_section.teacher.user.email
    def get_module(self, instance):
        return instance.assignment.module_section.module.name
    def get_module_type(self, instance):
        return instance.assignment.module_type
    
    def validate(self, attrs):
        #Check that the end time is after the start time
        if attrs['start_time'] > attrs['end_time']:
            raise serializers.ValidationError({'end_time':'The end time must be after the start time.'})
        #Check that all of the concerned groups exist in the assignment
        concerned_groups = attrs['concerned_groups']
        assignment_concerned_groups = attrs['assignment'].concerned_groups
        for group in concerned_groups:
            if not group in assignment_concerned_groups:
                raise serializers.ValidationError({'concerned_groups':'One of the specified groups does not exist in assignment.'})
        #Check that no other session is overlapping with this one.
        section = attrs['assignment'].module_section.section
        Q_section = Q(assignment__module_section__section=section)
        Q_overlap = Q(end_time__gte=attrs['start_time']) & Q(start_time__lte= attrs['end_time']) #Returns true if two sessions are overlapping.
        if 'id' in self.context.keys():
            #This is an update, we exclude this session from the search, otherwise we might find this session overlapping itself.
            Q_overlap = Q_overlap & ~Q(id=self.context['id'])
        if Session.objects.filter(Q_section,Q_overlap).exists():
            raise serializers.ValidationError({'start_time':'This session is overlapping another one.'})
        return attrs