import factory
from random import randint
from .models import *

# factory for Taxonomy model
# there are no tests for this factory as Taxonomy model is not queried at all inside api.py
class TaxonomyFactory(factory.django.DjangoModelFactory):
    # initialize values following data types declared in models.py
    taxa_id = 2711
    clade = "E"
    genus = "Citrus"
    species = "sinensis"
    # use Taxonomy model
    class Meta:
        model = Taxonomy

# factory for PFam model
class PFamFactory(factory.django.DjangoModelFactory):
    # initialize values following data types declared in models.py
    domain_id = "PF00360"
    domain_description = "senescenceregulator"
    # use PFam model
    class Meta:
        model = PFam

# factory for Protein model
class ProteinFactory(factory.django.DjangoModelFactory):
    # initialize values following data types declared in models.py
    protein_id = factory.Sequence(lambda n : 'P%d' % n + str(1))
    sequence = "MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA"
    length = randint(0, 99999)
    # use a SubFactory for Foreign Key
    taxonomy = factory.SubFactory(TaxonomyFactory)
    # use Protein model
    class Meta:
        model = Protein

# factory for TaxaLinkDomain model
class TaxaLinkDomainFactory(factory.django.DjangoModelFactory):
    # initialize values following data types declared in models.py
    taxa_id = 2711
    pfam_id = factory.SubFactory(PFamFactory)
    # use TaxaLinkDomain model
    class Meta:
        model = TaxaLinkDomain

# factory for TaxaLinkProtein model
class TaxaLinkProteinFactory(factory.django.DjangoModelFactory):
    # initialize values following data types declared in models.py
    taxa_id = 2711
    protein_id = factory.SubFactory(ProteinFactory)
    # use TaxaLinkProtein model
    class Meta:
        model = TaxaLinkProtein