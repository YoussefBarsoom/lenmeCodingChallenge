from django.db import models

class Investor(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField()

class Borrower(models.Model):
    name = models.CharField(max_length=200)

class Offer(models.Model):
    borrowerId = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    investorId = models.ForeignKey(Investor, on_delete=models.CASCADE,null=True,blank=True)
    loanAmount = models.IntegerField()
    loanPeriod = models.IntegerField()
    annualRate = models.IntegerField(null=True,blank=True)
    status = models.CharField(max_length=200)
    startDate = models.DateField(null=True,blank=True)
    monthsPaid = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.name+''
