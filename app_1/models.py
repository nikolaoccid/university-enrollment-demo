from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Korisnik(AbstractUser):
    ROLES = (('prof', 'profesor'), ('stu', 'student'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    role = models.CharField(max_length=50, choices=ROLES)
    status = models.CharField(max_length=50, choices=STATUS)


class Predmeti(models.Model):
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    # ovde može pucat -> limit choices to
    nositelj = models.ForeignKey(Korisnik, limit_choices_to={'role': 'prof'}, on_delete=models.CASCADE, null=True)


class Upisi(models.Model):
    STATUS_UPISA = (('upisan', 'Upisan'), ('polozen', 'Polozen'), ('izgubio', 'Izgubio potpis'))
    student = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status_upisa = models.CharField(max_length=50, choices=STATUS_UPISA)
