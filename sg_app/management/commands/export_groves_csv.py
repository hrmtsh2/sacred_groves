import csv
from django.core.management.base import BaseCommand
from django.utils import timezone

from sg_app.models import SacredGrove, PendingSacredGrove


class Command(BaseCommand):
    help = 'Export SacredGrove records (optionally pending submissions) to a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output', '-o',
            dest='output',
            default='sacred_groves.csv',
            help='Output CSV file path (default: sacred_groves.csv)'
        )
        parser.add_argument(
            '--include-pending',
            action='store_true',
            dest='include_pending',
            help='Include PendingSacredGrove records in the CSV (marked as source=pending)'
        )

    def handle(self, *args, **options):
        output_path = options['output']
        include_pending = options['include_pending']

        fieldnames = [
            'id', 'name', 'state', 'district', 'latitude', 'longitude',
            'area_coverage', 'altitude', 'description', 'source', 'submitted_at', 'user'
        ]

        qs_approved = SacredGrove.objects.all().order_by('id')

        rows_written = 0

        with open(output_path, mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Write approved/verified groves
            for g in qs_approved:
                writer.writerow({
                    'id': g.id,
                    'name': g.name,
                    'state': g.state,
                    'district': g.district,
                    'latitude': str(g.latitude),
                    'longitude': str(g.longitude),
                    'area_coverage': g.area_coverage,
                    'altitude': g.altitude,
                    'description': g.description,
                    'source': 'approved',
                    'submitted_at': '',
                    'user': ''
                })
                rows_written += 1

            # Optionally include pending submissions
            if include_pending:
                qs_pending = PendingSacredGrove.objects.all().order_by('id')
                for p in qs_pending:
                    submitted = p.submitted_at if getattr(p, 'submitted_at', None) else ''
                    writer.writerow({
                        'id': f"pending_{p.id}",
                        'name': p.name,
                        'state': p.state,
                        'district': p.district,
                        'latitude': str(p.latitude),
                        'longitude': str(p.longitude),
                        'area_coverage': p.area_coverage,
                        'altitude': p.altitude,
                        'description': p.description,
                        'source': 'pending',
                        'submitted_at': submitted,
                        'user': p.user.username if p.user else ''
                    })
                    rows_written += 1

        self.stdout.write(self.style.SUCCESS(f'Exported {rows_written} rows to {output_path}'))
