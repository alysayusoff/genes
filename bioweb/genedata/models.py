from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

# Taxonomy model
class Taxonomy(models.Model):
    # declare taxa_id as pk
    taxa_id = models.IntegerField(null=False, blank=False, primary_key=True)
    clade = models.CharField(max_length=1, default='E')
    genus = models.CharField(max_length=1000, null=False, blank=False)
    species = models.CharField(max_length=1000, null=False, blank=False)
    # return taxa_id
    def __int__(self):
        return self.taxa_id

# Protein model
class Protein(models.Model):
    # declare protein_id as pk
    protein_id = models.CharField(max_length=1000, null=False, blank=False, primary_key=True)
    sequence = models.CharField(max_length=1000, null=False, blank=False)
    length = models.IntegerField(null=False, blank=False)
    # declare taxonomy as foreign key pointing to Taxonomy model
    taxonomy = models.ForeignKey(Taxonomy, on_delete=DO_NOTHING, related_name='protein_taxa')
    # return protein_id
    def __str__(self):
        return self.protein_id

# PFam model
class PFam(models.Model):
    # declare domain_id as pk
    domain_id = models.CharField(max_length=1000, null=False, blank=False, primary_key=True)
    domain_description = models.CharField(max_length=1000, null=False, blank=False)
    # return domain_id
    def __str__(self):
        return self.domain_id

# Domain model
class Domain(models.Model):
    pfam_id = models.ForeignKey(PFam, on_delete=CASCADE)
    description = models.CharField(max_length=1000, null=False, blank=False)
    start = models.IntegerField(null=False, blank=False)
    stop = models.IntegerField(null=False, blank=False)
    # declare protein_id as foreign key pointing to Protein model
    protein_id = models.ForeignKey(Protein, on_delete=DO_NOTHING, related_name='domains')
    # return pfam_id
    def __str__(self):
        return self.pfam_id

# TaxaLinkProtein model
class TaxaLinkProtein(models.Model):
    taxa_id = models.IntegerField(null=False, blank=False)
    protein_id = models.CharField(max_length=1000, null=False, blank=False)
    # return taxa_id
    def __str__(self):
        return self.taxa_id

# TaxaLinkDomain
class TaxaLinkDomain(models.Model):
    taxa_id = models.IntegerField(null=False, blank=False)
    # declare pfam_id as foreign key pointing to PFam model
    pfam_id = models.ForeignKey(PFam, on_delete=DO_NOTHING)
    # return taxa_id
    def __str__(self):
        return self.taxa_id