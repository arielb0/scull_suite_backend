from django.core.management.base import BaseCommand
from wimm.models import Account, Summary
from datetime import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        summaries = []

        for account in Account.objects.filter(include_on_summary_section=True):
            summaries.append(
                Summary(
                    user=account.user, 
                    timestamp=datetime.now(),
                    account=account,
                    amount=account.amount
                )
            )

        Summary.objects.bulk_create(summaries)
