from django.db import models


class CollectedReview(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    review = models.TextField()
    doc_id = models.CharField(max_length=255, null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "stg_movie_reviews"
        managed = False

    def __str__(self):
        return self.title
