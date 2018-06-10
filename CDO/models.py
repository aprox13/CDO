from django.db import models
from CDO.vars import PERM_GUEST


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_login = models.CharField(max_length=40)
    user_password = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_surname = models.CharField(max_length=100, blank=True, null=True)
    user_permission = models.IntegerField(default=PERM_GUEST)

    class Meta:
        managed = True


class Organisation(models.Model):
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=100)
    org_date = models.CharField(max_length=100, blank=True, null=True)
    org_location = models.CharField(max_length=100, blank=True, null=True)
    org_about = models.TextField(max_length=1000, default='')
    org_dir_name = models.CharField(max_length=100, blank=True, null=True)
    org_dir_surname = models.CharField(max_length=100, blank=True, null=True)
    org_dir_birth = models.CharField(max_length=100, blank=True, null=True)

    def get_initial(self):
        org = self
        return {
            'org_name': org.org_name,
            'org_about': org.org_about,
            'org_date': org.org_date,
            'org_location': org.org_location,
            'org_dir_name': org.org_dir_name,
            'org_dir_surname': org.org_dir_surname,
            'org_dir_birth': org.org_dir_birth,
        }

    class Meta:
        managed = True
