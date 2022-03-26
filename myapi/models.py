from django.db import models


# Create your models here.

class approvals(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    dependants = models.IntegerField(default=0)
    applicant_income = models.IntegerField(default=0)
    coapplicant_income = models.IntegerField(default=0)
    loan_amount = models.IntegerField(default=0)
    loan_term = models.IntegerField(default=0)
    credit_history = models.IntegerField(default=0)
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    married_choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    graduated_choices = (
        ('Graduate', 'Graduate'),
        ('Not_Graduate', 'Not_Graduate')
    )
    self_employed_choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    property_choices = (
        ('Rural', 'Rural'),
        ('Semiurban', 'Semiurban'),
        ('Urban', 'Urban')
    )

    gender = models.CharField(max_length=15, choices=gender_choices)
    married = models.CharField(max_length=15, choices=married_choices)
    graduate_education = models.CharField(max_length=15, choices=graduated_choices)
    self_employed = models.CharField(max_length=15, choices=self_employed_choices)
    area = models.CharField(max_length=15, choices=property_choices)

    def __str__(self):
        return self.first_name
