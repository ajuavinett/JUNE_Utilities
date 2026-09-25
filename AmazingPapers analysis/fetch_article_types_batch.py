#!/usr/bin/env python3
"""
Batch script to fetch PubMed article metadata and PMC JATS article-types
Reads PMIDs from june_pmids.csv and outputs comprehensive results
"""

import requests
import xml.etree.ElementTree as ET
import csv
import time
from datetime import datetime

def fetch_pubmed_xml(pmid):
    """Fetch XML data for a PubMed article using E-utilities"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml',
        'rettype': 'abstract'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"  Error fetching PubMed data: {e}")
        return None

def extract_publication_types(xml_string):
    """Extract PublicationType elements from PubMed XML"""
    try:
        root = ET.fromstring(xml_string)
        pub_types = []
        for pub_type in root.findall('.//PublicationType'):
            pub_types.append({
                'type': pub_type.text,
                'ui': pub_type.get('UI', '')
            })
        return pub_types
    except Exception as e:
        print(f"  Error parsing publication types: {e}")
        return []

def get_pmcid_from_pubmed_xml(xml_string):
    """Extract PMCID from PubMed XML if available"""
    try:
        root = ET.fromstring(xml_string)
        for article_id in root.findall('.//ArticleId'):
            if article_id.get('IdType') == 'pmc':
                return article_id.text
        return None
    except Exception as e:
        print(f"  Error extracting PMCID: {e}")
        return None

def get_article_title(xml_string):
    """Extract article title from PubMed XML"""
    try:
        root = ET.fromstring(xml_string)
        title_elem = root.find('.//ArticleTitle')
        if title_elem is not None:
            return title_elem.text
        return "Title not found"
    except Exception as e:
        return "Error extracting title"

def fetch_pmc_xml(pmcid):
    """Fetch full-text XML from PubMed Central - tries multiple methods"""
    numeric_id = pmcid[3:] if pmcid.startswith('PMC') else pmcid
    
    # Method 1: Try OAI-PMH (full JATS XML)
    try:
        base_url = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
        params = {
            'verb': 'GetRecord',
            'identifier': f'oai:pubmedcentral.nih.gov:{numeric_id}',
            'metadataPrefix': 'pmc'
        }
        
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        if 'error' in response.text.lower() and 'idDoesNotExist' in response.text:
            pass  # Try next method
        else:
            return response.text
    except Exception as e:
        pass  # Try next method
    
    # Method 2: Try E-utilities efetch
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            'db': 'pmc',
            'id': numeric_id,
            'retmode': 'xml'
        }
        
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        if response.text and len(response.text) > 100:
            return response.text
    except Exception as e:
        pass
    
    return None

def extract_jats_article_type(xml_string):
    """Extract JATS article-type attribute from PMC XML"""
    try:
        root = ET.fromstring(xml_string)
        
        # Search for any element with tag ending in 'article' that has article-type attribute
        for elem in root.iter():
            tag_name = elem.tag
            # Remove namespace if present
            if '}' in tag_name:
                tag_name = tag_name.split('}')[1]
            
            if tag_name == 'article':
                article_type = elem.get('article-type')
                if article_type:
                    return article_type
        
        # Try with namespace awareness
        namespaces = {
            'jats': 'http://jats.nlm.nih.gov',
            'xlink': 'http://www.w3.org/1999/xlink',
            'mml': 'http://www.w3.org/1998/Math/MathML'
        }
        
        for ns_prefix, ns_uri in namespaces.items():
            article = root.find(f'.//{{{ns_uri}}}article')
            if article is not None:
                article_type = article.get('article-type')
                if article_type:
                    return article_type
        
        return None
    except Exception as e:
        print(f"  Error extracting JATS article-type: {e}")
        return None

# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("JUNE BATCH ARTICLE TYPE EXTRACTION")
    print("=" * 80)
    print()
    
    # Read input CSV
    input_file = "june_pmids.csv"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            articles = list(reader)
    except FileNotFoundError:
        print(f"ERROR: Could not find {input_file}")
        print("Please run june_pmid_search.py first to generate this file.")
        exit(1)
    
    print(f"Loaded {len(articles)} articles from {input_file}")
    print()
    
    results = []
    
    for i, article in enumerate(articles, 1):
        pmid = article['PMID']
        print(f"[{i}/{len(articles)}] Processing PMID: {pmid}")
        print(f"  {article['Author']} ({article['Year']}) - {article['Category']}")
        
        # Fetch PubMed XML
        pubmed_xml = fetch_pubmed_xml(pmid)
        
        if not pubmed_xml:
            print(f"  ✗ Failed to fetch PubMed XML")
            results.append({
                **article,
                'PubMed_Title': '',
                'PubMed_PublicationTypes': '',
                'PMC_ID': article.get('PMCID', ''),
                'JATS_ArticleType': '',
                'Status': 'Failed to fetch PubMed XML'
            })
            print()
            continue
        
        # Extract title and publication types
        title = get_article_title(pubmed_xml)
        pub_types = extract_publication_types(pubmed_xml)
        pub_types_str = '; '.join([pt['type'] for pt in pub_types])
        
        print(f"  Title: {title[:60]}...")
        print(f"  PubMed PublicationType(s): {pub_types_str if pub_types_str else 'None'}")
        
        # Get PMCID (use from CSV if available, otherwise extract)
        pmcid = article.get('PMC_ID', '').strip()
        if not pmcid:
            pmcid = get_pmcid_from_pubmed_xml(pubmed_xml)
        
        jats_type = None
        status = "Success - PubMed only"
        
        if pmcid:
            print(f"  PMC ID: {pmcid}")
            print(f"  Fetching PMC XML...")
            
            # Fetch PMC XML
            pmc_xml = fetch_pmc_xml(pmcid)
            
            if pmc_xml:
                # Extract JATS article-type
                jats_type = extract_jats_article_type(pmc_xml)
                
                if jats_type:
                    print(f"  ✓ JATS article-type: '{jats_type}'")
                    status = "Success - PubMed + PMC"
                else:
                    print(f"  ✗ Could not extract JATS article-type")
                    status = "PMC XML fetched but no article-type found"
            else:
                print(f"  ✗ Failed to fetch PMC XML")
                status = "PMC ID exists but XML fetch failed"
        else:
            print(f"  PMC: Not available")
        
        results.append({
            **article,
            'PubMed_Title': title,
            'PubMed_PublicationTypes': pub_types_str,
            'PMC_ID': pmcid if pmcid else '',
            'JATS_ArticleType': jats_type if jats_type else '',
            'Status': status
        })
        
        print()
        time.sleep(0.5)  # Be nice to NCBI servers
    
    # Save results to CSV
    print("=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"june_article_types_results_{timestamp}.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'PMID', 'Year', 'Author', 'Title', 'Category', 
            'PubMed_Title', 'PubMed_PublicationTypes', 
            'PMC_ID', 'JATS_ArticleType', 'Status'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✓ Results saved to: {output_file}")
    print()
    
    # Print summary statistics
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print()
    
    total = len(results)
    with_pmc = sum(1 for r in results if r['PMC_ID'])
    with_jats = sum(1 for r in results if r['JATS_ArticleType'])
    
    print(f"Total articles processed: {total}")
    print(f"Articles in PMC: {with_pmc} ({with_pmc/total*100:.1f}%)")
    print(f"Articles with JATS article-type: {with_jats} ({with_jats/total*100:.1f}%)")
    print()
    
    # Count by category
    print("By Category:")
    print("-" * 40)
    categories = {}
    for r in results:
        cat = r['Category']
        if cat not in categories:
            categories[cat] = {'total': 0, 'with_jats': 0}
        categories[cat]['total'] += 1
        if r['JATS_ArticleType']:
            categories[cat]['with_jats'] += 1
    
    for cat, counts in categories.items():
        print(f"  {cat}: {counts['total']} articles, {counts['with_jats']} with JATS type")
    print()
    
    # List unique JATS article-types found
    jats_types = {}
    for r in results:
        if r['JATS_ArticleType']:
            jat = r['JATS_ArticleType']
            if jat not in jats_types:
                jats_types[jat] = 0
            jats_types[jat] += 1
    
    if jats_types:
        print("JATS article-type values found:")
        print("-" * 40)
        for jat, count in sorted(jats_types.items()):
            print(f"  '{jat}': {count} article(s)")
    else:
        print("No JATS article-type values found")
    print()
    
    # List unique PubMed PublicationTypes
    pub_types = {}
    for r in results:
        if r['PubMed_PublicationTypes']:
            for pt in r['PubMed_PublicationTypes'].split('; '):
                if pt not in pub_types:
                    pub_types[pt] = 0
                pub_types[pt] += 1
    
    if pub_types:
        print("PubMed PublicationType values found:")
        print("-" * 40)
        for pt, count in sorted(pub_types.items()):
            print(f"  '{pt}': {count} article(s)")
    
    print()
    print("=" * 80)
    print(f"Complete results available in: {output_file}")
    print("=" * 80)
