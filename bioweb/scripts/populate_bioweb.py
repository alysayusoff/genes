import os
import sys
import django
import csv
from collections import defaultdict

# sys.path.append("C:/Users/alysa/Documents/SIM-UOL/Y3S1/CM3035 Advanced Web Development/vscode/mid-term-coursework/bioweb")
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioweb.settings')
django.setup()

from genedata.models import *

# assignment_data_sequences = "C:/Users/alysa/Documents/SIM-UOL/Y3S1/CM3035 Advanced Web Development/vscode/mid-term-coursework/data/assignment_data_sequences.csv"
# assignment_data_set = "C:/Users/alysa/Documents/SIM-UOL/Y3S1/CM3035 Advanced Web Development/vscode/mid-term-coursework/data/assignment_data_set.csv"
# pfam_descriptions = "C:/Users/alysa/Documents/SIM-UOL/Y3S1/CM3035 Advanced Web Development/vscode/mid-term-coursework/data/pfam_descriptions.csv"
assignment_data_sequences = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data\\assignment_data_sequences.csv')
assignment_data_set = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data\\assignment_data_set.csv')
pfam_descriptions = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data\\pfam_descriptions.csv')

# temporary sets
taxonomies = set()
proteins = set()
pfams = set()
domains = set()
sequenceSto = set() # reference set - NOT USED FOR CREATING RECORDS
taxadomain = set()
# open first file
with open(assignment_data_sequences) as csvfile:
    csv_file = csv.reader(csvfile, delimiter=',')
    for row in csv_file:
        # protein_id and sequences stored in reference set
        sequenceSto.add((row[0], row[1]))
# open second file
with open(assignment_data_set) as csvfile:
    dataSets = csv.reader(csvfile, delimiter=",")
    for row in dataSets:
        # i am splitting row[3] here because genus and species are combine into one, separated by " "
        gen_pair = row[3].split(" ")
        # here i am looping through gen_pair and checking if len(gen_pair) is more than 2
        for i in range(len(gen_pair)):
            # if i is more than two (len(gen_pair) > 2), add the rest of the gen_pair(s) into gen_pair[1]
            if i > 1:
                gen_pair[1] = gen_pair[1] + " " + gen_pair[i]
        # taxa_id, clade, genus, species stored
        taxonomies.add((row[1], row[2], gen_pair[0], gen_pair[1]))
        # taxa_id, domain_id stored
        taxadomain.add((row[1], row[5]))
        # loop through reference set
        for data in sequenceSto:
            # check if protein_id in csv exists in reference set
            if row[0] == data[0]:
                # if True...
                # protein_id, sequence, length, taxa_id stored
                proteins.add((data[0], data[1], row[8], row[1]))
                # domain_id, start, stop, description, protein_id stored
                domains.add((row[5], row[4], row[6], row[7], data[0]))
# open third file
with open(pfam_descriptions) as pfamDesc:
    pfamDesc = csv.reader(pfamDesc, delimiter=',')
    for row in pfamDesc:
        # domain_id and domain_description stored
        pfams.add((row[0], row[1]))
# the purpose of these delete commands are to make sure that if we run the script multiple times,
# we are making sure that we delete and replace the records - no duplicated and or skipped records
TaxaLinkDomain.objects.all().delete() # model with fk contraints - deleted first
Domain.objects.all().delete()         # model with fk contraints - deleted first
Protein.objects.all().delete()        # model with fk contraints - deleted first
PFam.objects.all().delete()
TaxaLinkProtein.objects.all().delete()
Taxonomy.objects.all().delete()
# initialize dictionaries to act as reference for instance data
taxonomy_rows = {}
protein_rows = {}
pfam_rows = {}
# loop through taxonomies
for data in taxonomies:
    # create Taxonomy object
    row = Taxonomy.objects.create(taxa_id=data[0], clade=data[1], genus=data[2], species=data[3])
    row.save()
    # save into dict
    taxonomy_rows[data[0]] = row
# loop through proteins
for data in proteins:
    # create TaxaLinkProtein object
    rowProteinLink = TaxaLinkProtein.objects.create(taxa_id=data[3], protein_id=data[0])
    rowProteinLink.save()
    # create Protein object, while referencing taxonomy_rows dict for instance data (fk)
    rowProtein = Protein.objects.create(
        protein_id=data[0], 
        sequence=data[1], 
        length=data[2], 
        taxonomy=taxonomy_rows[data[3]])
    rowProtein.save()
    # save into dict
    protein_rows[data[0]] = rowProtein
# loop through pfams
for data in pfams:
    # create PFam object
    row = PFam.objects.create(domain_id=data[0], domain_description=data[1])
    row.save()
    # save into dict
    pfam_rows[data[0]] = row
# loop through domains
for data in domains:
    # create Domain object, while refencing protein_rows dict for instance data (fk)
    row = Domain.objects.create(
        pfam_id=pfam_rows[data[0]], 
        description=data[1], 
        start=data[2], stop=data[3], 
        protein_id=protein_rows[data[4]])
    row.save()
# loop through taxadomain
for data in taxadomain:
    # create TaxaLinkDomain object, while refencing pfam_rows dict for instance data (fk)
    row = TaxaLinkDomain.objects.create(taxa_id=data[0], pfam_id=pfam_rows[data[1]])
    row.save()