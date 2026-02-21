from decimal import Decimal

from wimm.serializers import AccountSerializer, TransactionSerializer
from .models import Account, Summary, Transaction
from django.db.models import Sum, OuterRef, DecimalField, Subquery
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

def get_total_amount(user: User) -> Decimal:
    debited = Subquery(Transaction.objects.filter(source_account=OuterRef('id')).\
                   values('source_account').annotate(debited=Sum('amount')).\
                   values('debited'))
    
    credited = Subquery(Transaction.objects.filter(destination_account=OuterRef('id')).\
                    values('destination_account').annotate(credited=Sum('amount')).\
                    values('credited'))
    
    total = 0

    # Include user on filters.. , user=user
    account_amounts = Account.objects.filter(include_on_total_amount=True).\
                            annotate(amount=(Coalesce(Sum(credited), 0, output_field=DecimalField()) - Coalesce(Sum(debited), 0, output_field=DecimalField()))).\
                            values('amount')
    
    for account_amount in account_amounts:
        total += account_amount['amount']

    return total


def get_total_budget(user: User) -> Decimal:
    return Account.objects.aggregate(Sum('budget_percentage', output_field=DecimalField()))['budget_percentage__sum']


def get_summary(user: User, account: int):
    return Summary.objects.filter(user=user, account=account).values('timestamp', 'amount')


def get_last_transactions(user: User):
    last_transactions = Transaction.objects.filter(user=user).order_by('-timestamp')[:4]
    serializer = TransactionSerializer(last_transactions, many=True)
    return serializer.data


def get_accounts(user: User):
    accounts = Account.objects.filter(user=user, include_on_summary_section=True)
    serializer = AccountSerializer(accounts, many=True) # Create a AccountSummarySerializer
    return serializer.data
