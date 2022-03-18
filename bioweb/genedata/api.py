from rest_framework import mixins, generics
from rest_framework.response import Response
from .models import *
from .serializers import *

# api for http://127.0.0.1:8000/api/protein/
class ProteinCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    # query Protein model
    queryset = Protein.objects.all()
    # use ProteinSerializer
    serializer_class= ProteinSerializer
    # push new records
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# api for http://127.0.0.1:8000/api/protein/A0A016S8J7
class ProteinDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # query Protein model
    queryset = Protein.objects.all()
    # use ProteinAllSerializer (different than ProteinSerializer, which returns records WITHOUT domains)
    # ProtrainAllSerializer will return all values from Taxonomy, Protein, Domain and PFam models
    serializer_class = ProteinAllSerializer
    # retrieve records
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# api for http://127.0.0.1:8000/api/pfam/PF00360
class PFamDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # query PFam model
    queryset = PFam.objects.all()
    # use PFamSerializer
    serializer_class = PFamSerializer
    # retrieve records
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# api for http://127.0.0.1:8000/api/proteins/55661
class TaxonomyProteinDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # retrieve records
    def get(self, request, *args, **kwargs):
        # instead of using serializer, filter through TaxaLinkProtein using self.kwargs
        # retrieve only fields 'id' and 'protein_id'
        result = TaxaLinkProtein.objects.filter(taxa_id=self.kwargs['pk']).values('id', 'protein_id')
        # return result using Response
        return Response(result)

# api for http://127.0.0.1:8000/api/pfams/55661
class PFamTaxonomyDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # retrieve records
    def get(self, request, *args, **kwargs):
        # filter through TaxaLinkDomain using self.kwargs
        # retrieve only fields 'id' and 'pfam_id'
        result = TaxaLinkDomain.objects.filter(taxa_id=self.kwargs['pk']).values('id', 'pfam_id')
        # loop through retrieved results
        for row in result:
            # filter through PFam using row['pfam_id']
            # retrieve all fields and store temporarily
            temp = PFam.objects.filter(domain_id=row['pfam_id']).values()
            # replace the value in row['pfam_id'] with the temp result
            row['pfam_id'] = temp
        # return result using Response
        return Response(result)
        
# api for http://127.0.0.1:8000/api/coverage/A0A016S8J7
class Coverage(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # retrieve records
    def get(self, request, *args, **kwargs):
        # retrieve field 'length' from Protein using self.kwargs
        protein = Protein.objects.filter(protein_id=self.kwargs['pk']).values('length')
        # retrieve fields 'start' and 'stop' from Domain using self.kwargs
        domain = Domain.objects.filter(protein_id=self.kwargs['pk']).values('start', 'stop')
        # initialize global values
        sumStart = 0
        sumStop = 0
        sumLength = 0
        # looping through domain records
        for row in domain:
            # summate 'start'
            sumStart += row['start']
            # summate 'stop
            sumStop += row['stop']
        # looping through protein records
        for row in protein:
            # summate 'length'
            sumLength += row['length']
        # find coverage by doing (start-stop)/length
        result = (sumStart - sumStop) / sumLength
        # return result using Response
        return Response("coverage: " + str(abs(result)))