from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=140)
    is_income = models.BooleanField()
    budget = models.DecimalField(max_digits=9, decimal_places=2)
    specification_of = models.ForeignKey('Categories', null=True, related_name='category_specification')

    def __str__(self):
        return self.name

class Transactions(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey('Categories', related_name='transaction_category')
    specification = models.ForeignKey('Categories', related_name='transaction_specification')

class Balances(models.Model):
    date = models.DateTimeField()
    assets = models.DecimalField(max_digits=9, decimal_places=2)
    liabilities = models.DecimalField(max_digits=9, decimal_places=2)
    details = models.TextField()

    def __str__(self):
        return str(self.date)

class SearchTerms(models.Model):
    search_term = models.CharField(max_length=200)
    search_field = models.CharField(max_length=50)
    category = models.ForeignKey('Categories', related_name='search_term_category')
    specification = models.ForeignKey('Categories', related_name='search_term_specification')

    def __str__(self):
        return search_term

class UnprocessedTransactions(models.Model):
    payload = models.TextField()

    def __str__(self):
        return self.id
