from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # Baris bawaan Lab 9 kamu tetap dipertahankan
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description', 
            'location', 'status', 'reporter', 
            'created_at', 'updated_at'
        ]
        # Mengunci field waktu agar otomatis diatur oleh sistem database
        read_only_fields = ['created_at', 'updated_at']

    def get_reporter(self, obj):
        """
        Fungsi bawaan Lab 9 kamu untuk menampilkan nama pelapor.
        Jika di database field reporter kosong, tampil sebagai Warga Anonim.
        """
        if obj.reporter:
            return obj.reporter.username
        return "Warga Anonim"

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        
        # PENGAMAN UTAMA: Jika tidak ada request, atau user belum login (Anonim / Pas Registrasi), LANGSUNG AJALAH BYPASS
        if not request or not request.user or request.user.is_anonymous:
            return fields
            
        # PENGAMAN 1: JIKA CITIZEN LOGIN
        if hasattr(request.user, 'is_admin') and not request.user.is_admin:
            if 'status' in fields:
                fields['status'] = serializers.ChoiceField(
                    choices=[('DRAFT', 'Draft')], 
                    default='DRAFT'
                )
        
        # PENGAMAN 2: JIKA ADMIN LOGIN
        elif hasattr(request.user, 'is_admin') and request.user.is_admin:
            view = self.context.get('view')
            if view and hasattr(view, 'action') and view.action in ['retrieve', 'update', 'partial_update']:
                for field_name in ['title', 'category', 'description', 'location']:
                    if field_name in fields:
                        fields.pop(field_name)
                        
        return fields

    def validate_status(self, value):
        """
        Pengaman tingkat tinggi (Backend): Menolak jika Citizen mencoba menembak status 
        selain 'DRAFT' menggunakan tools luar seperti Postman.
        """
        request = self.context.get('request')
        if request and request.user and hasattr(request.user, 'is_admin'):
            if not request.user.is_admin and value != 'DRAFT':
                raise serializers.ValidationError("Citizen hanya diperbolehkan mengirim laporan dengan status 'DRAFT'!")
        return value