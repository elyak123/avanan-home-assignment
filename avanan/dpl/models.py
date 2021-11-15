from django.db import models


class Pattern(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=80, null=True, blank=True)
    pattern = models.TextField()

    class Meta:
        verbose_name = "Pattern"
        verbose_name_plural = "Patterns"

    def __str__(self):
        return self.name if hasattr(self, 'name') else self.pattern


class Leak(models.Model):
    message = models.TextField()
    content = models.TextField(null=True, blank=True)
    channel = models.CharField(max_length=15)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Leak"
        verbose_name_plural = "Leaks"

    def __str__(self):
        return self.message
