from rest_framework import serializers
from .models import *

# serializer for all fields in Taxonomy model
class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ['taxa_id', 'clade', 'genus', 'species']

# serializer for all fields in PFam model
class PFamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PFam
        fields = ['domain_id', 'domain_description']

# serializer for all fields in Domain and PFam model
class DomainSerializer(serializers.ModelSerializer):
    # pfam_id is an FK in Domain model, so we need to get the values by using def create()
    pfam_id = PFamSerializer()
    class Meta:
        model = Domain
        fields = ['pfam_id', 'description', 'start', 'stop']
    def create(self, validated_data):
        # get domain_id value
        pfam_data = self.initial_data.get('pfam_id')
        # retrieving data through comparing the pk in Pfam with pfam_id['domain_id']
        domain = Domain(**{**validated_data, 'pfam_id' : PFam.objects.get(pk = pfam_data['domain_id'])})
        domain.save()
        return domain

# serializer for all fields in Taxonomy, Protein, Domain and PFam models
class ProteinAllSerializer(serializers.ModelSerializer):
    # taxonomy is an FK in Protein model, so we need to get the values by using def create()
    taxonomy = TaxonomySerializer()
    # domains is an FK in Domain model that points to Protein model, the serializer will automatically 
    # retrieve matching rows
    domains = DomainSerializer(many=True) 
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']
    def create(self, validated_data):
        # get taxa_id value
        taxonomy_data = self.initial_data.get('taxonomy')
        # retrieving data through comparing the pk in Taxonomy with taxonomy_data['taxa_id']
        protein = Protein(**{**validated_data, 'taxonomy' : Taxonomy.objects.get(pk = taxonomy_data['taxa_id'])})
        protein.save()
        return protein
        
# serializer for all fields in Taxonomy and Protein models (this is only in used api.py for POST)
class ProteinSerializer(serializers.ModelSerializer):
    # taxonomy is an FK in Protein model, so we need to get the values by using def create()
    taxonomy = TaxonomySerializer()
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'length', 'taxonomy']
    def create(self, validated_data):
        # get taxa_id value
        taxonomy_data = self.initial_data.get('taxonomy')
        # retrieving data through comparing the pk in Taxonomy with taxonomy_data['taxa_id']
        protein = Protein(**{**validated_data, 'taxonomy' : Taxonomy.objects.get(pk = taxonomy_data['taxa_id'])})
        protein.save()
        return protein