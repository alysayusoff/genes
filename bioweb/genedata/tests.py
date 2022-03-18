import json
from django.urls import reverse
from rest_framework.test import APITestCase
from .model_factories import *
from .serializers import *
from .api import *

# Create your tests here.
# unit test for 127.0.0.1:8000/api/pfam/PF00360
class PFamSerializerTest(APITestCase):
    pfam1 = None
    pfamserializer = None

    def setUp(self):
        # create pfam1 instance
        self.pfam1 = PFamFactory.create(domain_id = "PF99999")
        # create pfamserializer instance
        self.pfamserializer = PFamSerializer(instance=self.pfam1)
    
    def tearDown(self):
        PFam.objects.all().delete()

    # testing for success of serializer
    def test_pfamSerializer(self):
        data = self.pfamserializer.data
        # check if the data is the same
        self.assertEqual(set(data.keys()), set(['domain_id', 'domain_description']))
    
    # testing for success of data
    def test_pfamSerializerDomainIDHasCorrectData(self):
        data = self.pfamserializer.data
        # check if the data is the same
        self.assertEqual(data['domain_id'], "PF99999")
# unit test for 127.0.0.1:8000/api/pfam/PF00360
class PFamTest(APITestCase):
    pfam1 = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        # create pfam1 instance
        self.pfam1 = PFamFactory.create(domain_id = "PF00360")
        # create a url that should succeed
        self.good_url = reverse('pfam_api', kwargs={'pk' : "PF00360"})
        # create a url that should fail
        self.bad_url = 'api/pfam/G2'
    
    def tearDown(self):
        PFam.objects.all().delete()

    # testing for success of returning values to the api
    def test_pfamDetailReturnSuccess(self):
        response = self.client.get(self.good_url, format=json)
        response.render()
        # check if return was successful (expected)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # check if 'domain_description' field exists in data
        self.assertTrue('domain_description' in data)
        # check if the values are the same/correct ones
        self.assertEqual(data['domain_description'], "senescenceregulator")
        
    # testing for failure of returning values to the api
    def test_pfamDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        # check if return failed (expected)
        self.assertEqual(response.status_code, 404)
# unit test for 127.0.0.1:8000/api/protein/ 
# and 127.0.0.1:8000/api/protein/A0A016S8J7 
# and 127.0.0.1:8000/api/coverage/A0A016S8J7
class ProteinSerializerTest(APITestCase):
    protein1 = None
    proteinserializer = None

    def setUp(self):
        # create protein1 instance
        self.protein1 = ProteinFactory.create(protein_id = "P1")
        # create proteinserializer instance
        self.proteinserializer = ProteinSerializer(instance=self.protein1)
    
    def tearDown(self):
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()
        TaxonomyFactory.reset_sequence(0)
        ProteinFactory.reset_sequence(0)

    # testing for success of serializer
    def test_proteinSerializer(self):
        data = self.proteinserializer.data
        # check if data is the same
        self.assertEqual(set(data.keys()), set(['protein_id', 'sequence', 'length', 'taxonomy']))

    # testing for success of data
    def test_proteinSerializerProteinIDHasCorrectData(self):
        data = self.proteinserializer.data
        # check if data is the same
        self.assertEqual(data['protein_id'], "P1")
# unit test for 127.0.0.1:8000/api/protein/ 
# and 127.0.0.1:8000/api/protein/A0A016S8J7 
# and 127.0.0.1:8000/api/coverage/A0A016S8J7
class ProteinTest(APITestCase):
    protein1 = None
    good_url = ''
    bad_url = ''

    def setUp(self): 
        # create protein1 instance
        self.protein1 = ProteinFactory.create(protein_id = "P1")
        # create a url that should succeed
        self.good_url = reverse('protein_api', kwargs={'pk' : "P1"})
        # create a url that should fail
        self.bad_url = 'api/protein/G2'

    def tearDown(self):
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()
        TaxonomyFactory.reset_sequence(0)
        ProteinFactory.reset_sequence(0)

    # testing for success of returning values to the api
    def test_proteinDetailReturnSuccess(self):
        response = self.client.get(self.good_url, format=json)
        response.render()
        # check if return was successful (expected)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # check if 'sequence' field exists at data
        self.assertTrue('sequence' in data)
        # check if values are the same/correct ones
        self.assertEqual(
            data['sequence'], 
            "MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA")

    # testing for failure of returning values to the api
    def test_proteinDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        # check if return failed (expected)
        self.assertEqual(response.status_code, 404)
# unit test for 127.0.0.1:8000/api/proteins/55661
class TaxonomyProteinTest(APITestCase):
    taxapro1 = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        # create a url that should succeed
        self.good_url = reverse('taxa_protein_api', kwargs={'pk' : 1})
        # create a url that should fail
        self.bad_url = "api/proteins/P"

    def tearDown(self):
        TaxaLinkProtein.objects.all().delete()

    # testing for success of returning values to the api
    def test_taxaproteinDetailReturnSuccess(self):
        response = self.client.get(self.good_url, format=json)
        response.render()
        # check if return was successful (expected)
        self.assertEqual(response.status_code, 200)
        
    # testing for failure of returning values to the api
    def test_taxaproteinDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        # check if return failed (expected)
        self.assertEqual(response.status_code, 404)

# unit test for 127.0.0.1:8000/api/pfams/55661
class TaxonomyDomainTest(APITestCase):
    taxado1 = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        # create a url that should succeed
        self.good_url = reverse('pfam_taxa_api', kwargs={'pk' : 1})
        # create a url that should fail
        self.bad_url = "api/pfams/P"

    def tearDown(self):
        TaxaLinkDomain.objects.all().delete()

    # testing for success of returning values to the api
    def test_taxaproteinDetailReturnSuccess(self):
        response = self.client.get(self.good_url, format=json)
        response.render()
        # check if return was successful (expected)
        self.assertEqual(response.status_code, 200)
        
    # testing for failure of returning values to the api
    def test_taxaproteinDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        # check if return failed (expected)
        self.assertEqual(response.status_code, 404)