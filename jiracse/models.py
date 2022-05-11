# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TbCse(models.Model):
    cseid = models.CharField(max_length=100)
    csename = models.CharField(max_length=1000)
    fullname = models.CharField(max_length=1000)
    customername = models.CharField(max_length=1000)
    csestatus = models.CharField(max_length=100)
    projectname = models.CharField(max_length=1000)
    version = models.CharField(max_length=10)
    maintenancedate = models.CharField(max_length=100)
    environmenttype = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tb_cse'


class TbEsdesk(models.Model):
    issueid = models.CharField(max_length=50)
    jiraid = models.CharField(max_length=50)
    esdeskname = models.CharField(max_length=50)
    issuetype = models.CharField(max_length=1000)
    issuestatus = models.CharField(max_length=1000)
    createdata = models.CharField(max_length=1000)
    epicid = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_esdesk'

