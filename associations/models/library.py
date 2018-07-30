from django.db import models

from authentication.models import User


class Library(models.Model):
    """
        Provides an interface to lend objects to people and to follow who has what
    """


class Object(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image = models.ImageField()
    comment = models.TextField()

    library = models.ForeignKey(Library, models.CASCADE)

    # By convention, -1 = unlimited number of this product.
    number_left = models.PositiveIntegerField(default=1)
    still_in_the_catalogue = models.BooleanField(default=True)

    # Can someone lend it on the site ?
    orderable_online = models.BooleanField(default=True)


class Loan(models.Model):
    class Meta:
        app_label = "association"
        db_table = "association_library_loan"

    object = models.OneToOneField(Object, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    loan_date = models.DateTimeField(auto_now=True)
    expected_return_date = models.DateTimeField(auto_now=False, null=True)
    real_return_date = models.DateTimeField(auto_now=False, null=True)

    STATUS = (
        ("ORDERED", "Commandé"),  # The person asked for the loan
        ("VALIDATED", "Validé"),  # The owner confirms it can honor the request
        ("DELIVERED", "Délivré"),  # The product has been given. The order cannot be CANCELLED then
        ("CANCELLED", "Annulé"),  # The person cancels the order
        ("RETURNED", "Rendu"),  # The loan is finished
    )
    status = models.CharField(choices=STATUS)
