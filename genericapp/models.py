from django.db import models

class SearchDomain(models.Model):
    domain_column = models.CharField(blank=False, null=False, unique=True, max_length=20)
    value = models.CharField(blank=False, null=False, max_length=1024)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str({
            "domain_column": self.domain_column,
            "value": self.value
        })
