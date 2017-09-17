from django.db import models

# This class stores all the categories for transactions
# It stores both an overarching category and the specification of these
class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=140)
    is_income = models.BooleanField()
    budget = models.DecimalField(max_digits=9, decimal_places=2)
    specification_of = models.ForeignKey('Categories', null=True, related_name='category_specification')

    def __str__(self):
        return self.name

# This class stores transactions that have been made
class Transactions(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey('Categories', related_name='transaction_category')
    specification = models.ForeignKey('Categories', related_name='transaction_specification')

# This class stores the balance of a balanceitem in a particular month
# In the code elsewhere it is made so that the date is always the first of the month
class Balances(models.Model):
    item = models.ForeignKey('BalanceItems', related_name='balances_balance_items')
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.date) + " " + str(self.item.name)

# This class stores the available categories of balances
class BalanceItems(models.Model):
    name = models.CharField(max_length=100, unique=True)
    asset = models.BooleanField()

    def __str__(self):
        return self.name

# This class stores the terms where you can search on in
class SearchTerms(models.Model):
    dataset = models.ForeignKey('Datasets', related_name='search_term_dataset')
    term = models.CharField(max_length=200)
    field = models.CharField(max_length=50)
    category = models.ForeignKey('Categories', related_name='search_term_category')
    specification = models.ForeignKey('Categories', related_name='search_term_specification')

    def __str__(self):
        return self.term

# This class stores the various sources of data
class Datasets(models.Model):
    name = models.CharField(max_length=20)
    date_field = models.CharField(max_length=20)
    amount_field = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# This class stores transactions that the automated stuff couldn't categorize
# The user needs to take a look a these to categorize them
class UnprocessedTransactions(models.Model):
    payload = models.TextField()
    dataset = models.ForeignKey('Datasets', related_name='unprocessed_transactions_dataset')

    def __str__(self):
        return self.id
