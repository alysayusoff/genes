from django.urls import include, path
from . import api

urlpatterns = [
    # add a new record
    path('api/protein/', api.ProteinCreate.as_view(), name='create_protein'),
    # return the protein sequence and all we know about it
    path('api/protein/<str:pk>', api.ProteinDetails.as_view(), name='protein_api'),
    # return the domain and it's description
    path('api/pfam/<str:pk>', api.PFamDetails.as_view(), name='pfam_api'),
    # return a list of all proteins for a given organism
    path('api/proteins/<int:pk>', api.TaxonomyProteinDetails.as_view(), name='taxa_protein_api'),
    # return a list of all domains in all the proteins for a given organism
    path('api/pfams/<int:pk>', api.PFamTaxonomyDetails.as_view(), name='pfam_taxa_api'),
    # return the domain coverage for a given protein
    path('api/coverage/<str:pk>', api.Coverage.as_view(), name='coverage_api'),
]