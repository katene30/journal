from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date, timedelta

from django.utils import timezone

from .models import JournalEntry
from .serializers import (
    JournalEntryListSerializer,
    JournalEntryScalesSerializer,
    JournalEntrySerializer,
)

MAX_RANGE_DAYS = 366


class JournalEntryViewSet(viewsets.ModelViewSet):
    """API endpoint for journal entries."""
    serializer_class = JournalEntrySerializer

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return JournalEntryListSerializer
        return JournalEntrySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get or create today's entry."""
        # localdate() uses settings.TIME_ZONE; now().date() would be the UTC date
        today = timezone.localdate()
        entry, created = JournalEntry.objects.get_or_create(
            user=request.user,
            date=today,
        )
        serializer = self.get_serializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='by-date/(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})')
    def by_date(self, request, date=None):
        """Get or create entry for a specific date."""
        from datetime import datetime
        try:
            parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        entry, created = JournalEntry.objects.get_or_create(
            user=request.user,
            date=parsed_date,
        )
        serializer = self.get_serializer(entry)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent entries (last 7 days)."""
        entries = self.get_queryset()[:7]
        serializer = JournalEntryListSerializer(entries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def range(self, request):
        """Scale values for entries between ?start= and ?end= (YYYY-MM-DD, inclusive).

        Defaults to the last 30 days. Read-only: unlike today/by-date it never
        creates entries.
        """
        try:
            end = date.fromisoformat(request.query_params['end']) if 'end' in request.query_params else timezone.localdate()
            start = date.fromisoformat(request.query_params['start']) if 'start' in request.query_params else end - timedelta(days=29)
        except ValueError:
            return Response({'detail': 'Dates must be YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        if start > end:
            return Response({'detail': 'start must be on or before end.'}, status=status.HTTP_400_BAD_REQUEST)
        if (end - start).days + 1 > MAX_RANGE_DAYS:
            return Response({'detail': f'Range can be at most {MAX_RANGE_DAYS} days.'}, status=status.HTTP_400_BAD_REQUEST)

        entries = self.get_queryset().filter(date__range=(start, end)).order_by('date')
        return Response({
            'start': start.isoformat(),
            'end': end.isoformat(),
            'entries': JournalEntryScalesSerializer(entries, many=True).data,
        })
