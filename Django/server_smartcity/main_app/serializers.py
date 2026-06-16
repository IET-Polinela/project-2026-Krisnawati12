from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'description',
            'category',
            'status',
            'location',
            'created_at',
            'updated_at',
            'reporter',
            'is_owner',
        ]
        read_only_fields = [
            'created_at',
            'updated_at',
            'reporter',
            'is_owner',
        ]

    def get_reporter(self, obj):
        request = self.context.get('request')

        if request:
            tab = request.query_params.get('tab', None)

            if tab == 'feed' and obj.reporter != request.user:
                return "Warga Anonim"

        if obj.reporter:
            return obj.reporter.username

        return "Warga Anonim"

    def get_is_owner(self, obj):
        request = self.context.get('request')

        if not request or not hasattr(request, 'user'):
            return False

        return request.user == getattr(obj, 'reporter', None)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')

        if not request or not request.user or request.user.is_anonymous:
            return fields

        if hasattr(request.user, 'is_admin') and not request.user.is_admin:
            if 'status' in fields:
                fields['status'] = serializers.ChoiceField(
                    choices=[
                        ('DRAFT', 'Draft'),
                        ('REPORTED', 'Reported'),
                    ],
                    default='REPORTED',
                    required=False,
                )

        elif hasattr(request.user, 'is_admin') and request.user.is_admin:
            view = self.context.get('view')

            if view and hasattr(view, 'action') and view.action in ['update', 'partial_update']:
                editable_fields = {'status'}

                for field_name in list(fields.keys()):
                    if field_name not in editable_fields:
                        fields.pop(field_name)

        return fields

    def validate_status(self, value):
        request = self.context.get('request')

        if not request or not request.user or request.user.is_anonymous:
            return value

        if getattr(request.user, 'is_admin', False):
            allowed_transitions = {
                'REPORTED': ['REPORTED', 'VERIFIED'],
                'VERIFIED': ['VERIFIED', 'IN_PROGRESS'],
                'IN_PROGRESS': ['IN_PROGRESS', 'RESOLVED'],
                'RESOLVED': ['RESOLVED'],
            }

            current_status = getattr(self.instance, 'status', None)
            allowed_status = allowed_transitions.get(
                current_status,
                ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED'],
            )

            if value not in allowed_status:
                raise serializers.ValidationError(
                    "Admin hanya boleh mengubah status laporan sesuai alur berikutnya."
                )

        else:
            allowed_status = ['DRAFT', 'REPORTED']

            if value not in allowed_status:
                raise serializers.ValidationError(
                    "Citizen hanya boleh menggunakan status DRAFT atau REPORTED."
                )

        return value