#!/usr/bin/env python3
"""
Script to search for PMIDs of JUNE AMAZING PAPERS and MEDIA REVIEWS articles (2020-2024)
and extract their JATS article-types
"""

import requests
import xml.etree.ElementTree as ET
import time

# List of AMAZING PAPERS and MEDIA REVIEWS articles from JUNE (2018-2025)
articles = [
    # 2024
    {"year": 2024, "author": "Chivero ET", "title": "Primary Literature for Teaching Neuroimmunology", "type": "AMAZING PAPERS"},
    {"year": 2024, "author": "Harris Bozer AL", "title": "Introducing BRAINOER", "type": "MEDIA REVIEWS"},
    
    # 2023
    {"year": 2023, "author": "Horn CM", "title": "Remyelination and Ageing", "type": "AMAZING PAPERS"},
    {"year": 2023, "author": "Payne AJ", "title": "Teaching Synaptic Transmission Using Primary Literature", "type": "AMAZING PAPERS"},
    {"year": 2023, "author": "Caccamo A", "title": "Unlocking Hidden Awareness fMRI", "type": "AMAZING PAPERS"},
    
    # 2022
    {"year": 2022, "author": "Petukhov V", "title": "Exploring the neural cell nucleus", "type": "AMAZING PAPERS"},
    
    # 2021
    {"year": 2021, "author": "Wilson JM", "title": "Examining Empathy through Consolation Behavior in Prairie Voles", "type": "AMAZING PAPERS"},
    {"year": 2021, "author": "Strathern L", "title": "Mapping cognition with fMRI", "type": "AMAZING PAPERS"},
    {"year": 2021, "author": "Sane M", "title": "Teaching neural circuits using Drosophila aggression", "type": "AMAZING PAPERS"},
    {"year": 2021, "author": "Takemori T", "title": "Using primary literature behavioral genetics", "type": "AMAZING PAPERS"},
    
    # 2020
    {"year": 2020, "author": "McManus J", "title": "Sparse Neural Representation of Odor Predicts Learning", "type": "AMAZING PAPERS"},
    {"year": 2020, "author": "Delgado-Sanchez A", "title": "Does It Feel Right or Wrong Neuroscience of Moral Judgement", "type": "AMAZING PAPERS"},
    {"year": 2020, "author": "Ramos RL", "title": "Primary Literature In Clinical Neuroscience", "type": "AMAZING PAPERS"},
    {"year": 2020, "author": "Elliott D", "title": "The Legacy of the Kennard Principle", "type": "AMAZING PAPERS"},
    {"year": 2020, "author": "Housman HAR", "title": "Exploring Neuroplasticity in the Classroom", "type": "AMAZING PAPERS"},
    {"year": 2020, "author": "Riegel DC", "title": "Discovering Memory Using Sea Slugs", "type": "AMAZING PAPERS"},
    
    # 2019
    {"year": 2019, "author": "Haun HL", "title": "Using primary literature to teach neuroscience", "type": "AMAZING PAPERS"},
    {"year": 2019, "author": "Carney KE", "title": "Teaching neuroscience with primary literature", "type": "AMAZING PAPERS"},
    
    # 2018
    {"year": 2018, "author": "Lom B", "title": "Review of Developmental Neurobiology by Lynne M Bianchi", "type": "MEDIA REVIEWS"},
    {"year": 2018, "author": "Palissery GK", "title": "Six Autobiographies and Two Realistic Fiction Books", "type": "MEDIA REVIEWS"},
]

def search_pubmed_for_pmid(author, title, year):
    """
    Search PubMed for an article and return its PMID
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # Construct search query
    # Search for author, year, and key words from title
    search_terms = f"{author}[Author] AND {year}[PDAT] AND Journal Undergraduate Neuroscience"
    
    params = {
        'db': 'pubmed',
        'term': search_terms,
        'retmode': 'xml',
        'retmax': 5
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        id_list = root.find('.//IdList')
        
        if id_list is not None and len(id_list) > 0:
            pmid = id_list[0].text
            return pmid
        else:
            return None
            
    except Exception as e:
        print(f"  Error searching: {e}")
        return None

def fetch_pubmed_xml(pmid):
    """
    Fetch PubMed XML for a given PMID
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  Error fetching: {e}")
        return None

def extract_publication_types(xml_string):
    """
    Extract PublicationType from PubMed XML
    """
    try:
        root = ET.fromstring(xml_string)
        pub_types = []
        for pub_type in root.findall('.//PublicationType'):
            pub_types.append(pub_type.text)
        return pub_types
    except:
        return []

def get_pmcid_from_pubmed_xml(xml_string):
    """
    Extract PMCID from PubMed XML
    """
    try:
        root = ET.fromstring(xml_string)
        for article_id in root.findall('.//ArticleId'):
            if article_id.get('IdType') == 'pmc':
                return article_id.text
        return None
    except:
        return None

print("=" * 80)
print("JUNE AMAZING PAPERS & MEDIA REVIEWS: JATS article-type Analysis (2018-2025)")
print("=" * 80)
print()

results = []

for i, article in enumerate(articles, 1):
    print(f"[{i}/{len(articles)}] Searching: {article['author']} ({article['year']})")
    print(f"     Title: {article['title'][:60]}...")
    
    # Search for PMID
    pmid = search_pubmed_for_pmid(article['author'], article['title'], article['year'])
    
    if pmid:
        print(f"     ✓ Found PMID: {pmid}")
        
        # Fetch PubMed XML
        pubmed_xml = fetch_pubmed_xml(pmid)
        
        if pubmed_xml:
            # Extract PublicationType
            pub_types = extract_publication_types(pubmed_xml)
            
            # Get PMCID
            pmcid = get_pmcid_from_pubmed_xml(pubmed_xml)
            
            results.append({
                'article': article,
                'pmid': pmid,
                'pmcid': pmcid,
                'pubmed_pubtypes': pub_types,
                'jats_type': None  # Will be filled if PMC available
            })
            
            print(f"     PubMed PublicationType(s): {', '.join(pub_types) if pub_types else 'None'}")
            if pmcid:
                print(f"     PMC ID: {pmcid} (available for JATS extraction)")
            else:
                print(f"     PMC: Not available")
        else:
            print(f"     ✗ Could not fetch PubMed XML")
    else:
        print(f"     ✗ PMID not found")
        results.append({
            'article': article,
            'pmid': None,
            'pmcid': None,
            'pubmed_pubtypes': [],
            'jats_type': None
        })
    
    print()
    time.sleep(0.5)  # Be nice to NCBI servers

# Print summary
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

print(f"Total articles searched: {len(articles)}")
print(f"PMIDs found: {sum(1 for r in results if r['pmid'])}")
print(f"Articles in PMC: {sum(1 for r in results if r['pmcid'])}")
print()

print("Articles with PMIDs:")
print("-" * 80)
for r in results:
    if r['pmid']:
        print(f"PMID {r['pmid']}: {r['article']['author']} ({r['article']['year']}) - {r['article']['type']}")
        if r['pubmed_pubtypes']:
            print(f"  PubMed Types: {', '.join(r['pubmed_pubtypes'])}")
        if r['pmcid']:
            print(f"  PMC: {r['pmcid']}")
print()

print("Articles NOT found in PubMed:")
print("-" * 80)
for r in results:
    if not r['pmid']:
        print(f"  {r['article']['author']} ({r['article']['year']}) - {r['article']['title'][:60]}")
print()

print("=" * 80)
print("SAVING RESULTS TO FILE")
print("=" * 80)

# Save results to CSV file for batch processing
import csv

output_file = "june_pmids.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Write header
    writer.writerow(['PMID', 'Year', 'Author', 'Title', 'Category', 'PMC_ID'])
    
    # Write data
    for r in results:
        if r['pmid']:  # Only include articles with PMIDs
            writer.writerow([
                r['pmid'],
                r['article']['year'],
                r['article']['author'],
                r['article']['title'],
                r['article']['type'],
                r['pmcid'] if r['pmcid'] else ''
            ])

print(f"✓ PMIDs saved to: {output_file}")
print(f"  Found {sum(1 for r in results if r['pmid'])} PMIDs out of {len(articles)} articles")
print()
print("Next step: Run fetch_article_types_batch.py to extract JATS article-types")
print("=" * 80)
