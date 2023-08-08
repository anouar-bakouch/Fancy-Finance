from django.db import models
from rest_framework import serializers # Importing serializers

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    firstName = models.CharField(max_length=255, default='no name')
    lastName = models.CharField(max_length=255, default='no name')
    pathPhoto = models.ImageField(upload_to='static/images', default='images/None/no-img.jpg')
    def __str__(self):
        return self.username

class Budget(models.Model):

    IDEIMPST = models.IntegerField(primary_key=True, default=0 )
    MONTSTRU = models.FloatField()
    MONTRAPP = models.FloatField()
    MOISSOLD = models.DateField( default='2021-01-01')
    CODTYPAC = models.CharField(max_length=50, default='no code')
    LIBACTGE = models.CharField(max_length=50, default='no libelle')
    Budgets = models.FloatField()
    User = models.ForeignKey(to=User, on_delete=models.CASCADE,null=True)    
    budgetphoto = models.ImageField(upload_to='static/items', default='images/None/no-img.jpg')
    
    # String representation of the model
    def __str__(self):
        return str(self.IDEIMPST) + ' ' + str(self.LIBACTGE)
    
    # create method to create a new budget
    def create(self, validated_data):
        return Budget.objects.create(**validated_data)
    
    def get(self, instance):
        return instance
    
    def UserInfo(self, instance):
        return instance.User
    
    # update method to update an existing budget
    def update(self, instance, validated_data):
        instance.IDEIMPST = validated_data.get('IDEIMPST', instance.IDEIMPST)
        instance.MONTSTRU = validated_data.get('MONTSTRU', instance.MONTSTRU)
        instance.MONTRAPP = validated_data.get('MONTRAPP', instance.MONTRAPP)
        instance.MOISSOLD = validated_data.get('MOISSOLD', instance.MOISSOLD)
        instance.CODTYPAC = validated_data.get('CODTYPAC', instance.CODTYPAC)
        instance.LIBACTGE = validated_data.get('LIBACTGE', instance.LIBACTGE)
        instance.Budgets = validated_data.get('Budgets', instance.Budgets)
        instance.User = validated_data.get('User', instance.User)
        instance.budgetphoto = validated_data.get('budgetPhoto', instance.budgetPhoto)
        

        instance.save()
        return instance


