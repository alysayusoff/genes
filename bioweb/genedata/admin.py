from django.contrib import admin
from .models import *

# display models in admin site
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('taxa_id', 'clade', 'genus', 'species')

class ProteinAdmin(admin.ModelAdmin):
    list_display = ('protein_id', 'length', 'sequence')

class DomainAdmin(admin.ModelAdmin):
    list_display = ('pfam_id', 'description', 'start', 'stop')

class PFamAdmin(admin.ModelAdmin):
    list_display = ('domain_id', 'domain_description')

class TaxaLinkDomainAdmin(admin.ModelAdmin):
    list_display = ('taxa_id', 'pfam_id')

class TaxaLinkProteinAdmin(admin.ModelAdmin):
    list_display = ('taxa_id', 'protein_id')

# register models
admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Protein, ProteinAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(PFam, PFamAdmin)
admin.site.register(TaxaLinkDomain, TaxaLinkDomainAdmin)
admin.site.register(TaxaLinkProtein, TaxaLinkProteinAdmin)