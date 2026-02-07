from decimal import Decimal
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef, Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils.functional import cached_property


class Account(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length = 255)
    goal_description = models.TextField()
    goal_amount = models.DecimalField(max_digits = 9, decimal_places = 2)
    budget_percentage = models.DecimalField(max_digits = 5, decimal_places = 2)
    include_on_summary_section = models.BooleanField()
    include_on_total_amount = models.BooleanField()
    color = models.IntegerField()

    @property
    def amount(self) -> Decimal:
        
        debited = Subquery(Transaction.objects.filter(source_account=OuterRef('pk')).\
                   values('source_account').annotate(debited=Sum('amount')).\
                   values('debited'))
        
        credited = Subquery(Transaction.objects.filter(destination_account=OuterRef('pk')).\
                    values('destination_account').annotate(credited=Sum('amount')).\
                    values('credited'))
        
        return Account.objects.filter(pk=self.pk).annotate(amount=(Coalesce(Sum(credited), 0, output_field=DecimalField())\
        - Coalesce(Sum(debited), 0, output_field=DecimalField()))).values('amount')[0]['amount']


class Transaction(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    timestamp = models.DateTimeField()
    amount = models.DecimalField(max_digits = 9, decimal_places = 2)
    source_account = models.ForeignKey(Account, models.CASCADE, related_name = 'source_accounts')
    destination_account = models.ForeignKey(Account, models.CASCADE, related_name = 'destination_accounts')
    description = models.TextField()

    @cached_property
    def source_account_name(self) -> string:
        source_account = Account.objects.get(pk=self.source_account.pk)
        return source_account.name
    
    @cached_property
    def destination_account_name(self) -> string:
        destination_account = Account.objects.get(pk=self.destination_account.pk)
        return destination_account.name

    @cached_property
    def keywords(self) -> string:
        return f'{self.timestamp}; {self.amount}; {self.source_account_name}; {self.destination_account_name}; {self.description}'
    

class Configuration(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    currency = models.CharField(max_length=4)
    currency_display = models.CharField(16)
    locale = models.CharField(max_length=16)


class Summary(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    timestamp = models.DateTimeField()
    account = models.ForeignKey(Account, models.CASCADE)
    amount = models.DecimalField(max_digits = 9, decimal_places = 2)
