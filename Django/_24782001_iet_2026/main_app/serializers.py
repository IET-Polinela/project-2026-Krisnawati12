from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # Baris bawaan Lab 9 tetap dipertahankan
    reporter = serializers.SerializerMethodField()
    
    # -----------------------------------------------------------------
    # TAMBAHAN BARU LAB 12: Daftarkan Field is_owner
    # -----------------------------------------------------------------
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        # Pastikan 'is_owner' dimasukkan ke dalam list fields
        fields = [
            'id', 'title', 'description', 'category', 'status', 'location',
            'created_at', 'updated_at', 'reporter', 'is_owner',
        ]
        # Mengunci field waktu agar otomatis diatur oleh sistem database
        read_only_fields = ['created_at', 'updated_at']

    # -----------------------------------------------------------------
    # MODIFIKASI LAB 12: Pengaman Nama Pelapor Berbasis Tab Menu
    # -----------------------------------------------------------------
    def get_reporter(self, obj):
        request = self.context.get('request')
        if request:
            # Membaca parameter ?tab= yang sedang diakses di URL oleh SPA
            tab = request.query_params.get('tab', None)
            
            # Jika tab yang dibuka adalah 'feed' (Feed Kota Publik)
            if tab == 'feed':
                # Cek jika laporan tersebut BUKAN miliknya, langsung sensor namanya
                if obj.reporter != request.user:
                    return "Warga Anonim"

        # Kondisi default atau saat di tab "Laporan Saya", tampilkan nama aslinya
        if obj.reporter:
            return obj.reporter.username
        return "Warga Anonim"

    # -----------------------------------------------------------------
    # TAMBAHAN BARU LAB 12: Fungsi Pengecekan Kepemilikan Laporan
    # -----------------------------------------------------------------
    def get_is_owner(self, obj):
        request = self.context.get('request', None)
        if not request or not hasattr(request, 'user'):
            return False
        return request.user == getattr(obj, 'reporter', None)

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
                    choices=[
                        ('DRAFT', 'Draft'),
                        ('REPORTED', 'Reported')
                    ],
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

        request = self.context.get('request')

        if (
            request and
            request.user and
            hasattr(request.user, 'is_admin') and
            not request.user.is_admin
        ):

            allowed_status = ['DRAFT', 'REPORTED']

            if value not in allowed_status:
                raise serializers.ValidationError(
                    "Citizen hanya boleh menggunakan status DRAFT atau REPORTED."
                )

        return value