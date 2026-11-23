"""Account-level endpoints: export everything, delete everything."""
import csv
import io
import json

from django.contrib.auth import logout
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from entries.serializers import JournalEntrySerializer

EXPORT_FORMATS = ('json', 'csv')


def _attachment(content, content_type, filename):
    response = HttpResponse(content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    # Journal data: never let a shared or browser cache keep a copy
    response['Cache-Control'] = 'no-store'
    return response


class AccountExportView(APIView):
    """GET /api/account/export/?file=json|csv: everything stored about the user.

    JSON is the complete record (account details plus every entry). CSV is the
    entries only, one row per day, for opening in a spreadsheet.
    The query param isn't called `format` because DRF reserves that name.
    """

    def get(self, request):
        file_format = request.query_params.get('file', 'json')
        if file_format not in EXPORT_FORMATS:
            return Response(
                {'detail': f'file must be one of: {", ".join(EXPORT_FORMATS)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        entries = JournalEntrySerializer(user.entries.order_by('date'), many=True).data
        now = timezone.now()
        filename = f'hauora-journal-{timezone.localdate():%Y-%m-%d}.{file_format}'

        if file_format == 'csv':
            fields = [f for f in JournalEntrySerializer.Meta.fields if f != 'id']
            buffer = io.StringIO()
            # BOM so Excel reads UTF-8 and shows macrons correctly
            buffer.write('﻿')
            writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(entries)
            return _attachment(buffer.getvalue(), 'text/csv; charset=utf-8', filename)

        data = {
            'exported_at': now.isoformat(),
            'account': {
                'email': user.email,
                'date_joined': user.date_joined.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
            },
            'entries': entries,
        }
        return _attachment(
            json.dumps(data, indent=2, ensure_ascii=False),
            'application/json; charset=utf-8',
            filename,
        )


class AccountDeleteView(APIView):
    """POST /api/account/delete/ {password}: permanently delete the account.

    The password is required even though the session is already logged in, so
    an unattended logged-in device can't be used to wipe someone's journal.
    Entries and email records are removed by the user's cascading foreign keys.
    """
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'account_delete'

    def post(self, request):
        password = request.data.get('password') or ''
        user = request.user
        if not user.check_password(password):
            return Response(
                {'password': ['Incorrect password.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logout(request)
        # Model.delete() runs the whole cascade in one transaction
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
