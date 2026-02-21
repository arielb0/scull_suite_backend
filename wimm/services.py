from wimm.selectors import get_total_budget
from .models import Account, Transaction
from django.contrib.auth.models import User
from datetime import datetime


def apply_budget(user: User, source_account: Account):
    if source_account.amount == 0:
        raise Exception('Source account must have a valid amount greater than zero.')
    if get_total_budget(user) != 1:
        raise Exception(f'Budget is not equal to 100%. The actual value is {get_total_budget(user * 100)}%')

    accounts = Account.objects.filter(budget_percentage__gt=0).exclude(pk=source_account.pk)
    source_account_amount = source_account.amount
    transactions = []

    for account in accounts:
        
        transactions.append(
            Transaction(
                user = user,
                timestamp = datetime.now(),
                amount = source_account_amount * account.budget_percentage,
                source_account = source_account,
                destination_account = account,
                description = f'Moved the {account.budget_percentage * 100}% from "{source_account.name}" to "{account.name}".'
            )
        )

    Transaction.objects.bulk_create(transactions)
