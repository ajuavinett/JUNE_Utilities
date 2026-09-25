#!/usr/bin/env python3
"""
Script to fetch PubMed article metadata and PMC full-text XML
Extracts both PublicationType (PubMed) and article-type (JATS/PMC)
"""

import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def fetch_pubmed_xml(pmid):
    """
    Fetch XML data for a PubMed article using E-utilities
    
    Args:
        pmid: PubMed ID (PMID) as string or integer
    
    Returns:
        XML content as string
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml',
        'rettype': 'abstract'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PubMed data: {e}")
        return None

def extract_publication_types(xml_string):
    """
    Extract PublicationType elements from PubMed XML
    
    Returns:
        List of publication types
    """
    try:
        root = ET.fromstring(xml_string)
        
        # Find all PublicationType elements
        pub_types = []
        for pub_type in root.findall('.//PublicationType'):
            pub_types.append({
                'type': pub_type.text,
                'ui': pub_type.get('UI', '')
            })
        
        return pub_types
    except Exception as e:
        print(f"Error parsing publication types: {e}")
        return []

def get_pmcid_from_pubmed_xml(xml_string):
    """
    Extract PMCID from PubMed XML if available
    
    Returns:
        PMCID string or None
    """
    try:
        root = ET.fromstring(xml_string)
        
        # Look for PMC ID in ArticleIdList
        for article_id in root.findall('.//ArticleId'):
            if article_id.get('IdType') == 'pmc':
                return article_id.text
        
        return None
    except Exception as e:
        print(f"Error extracting PMCID: {e}")
        return None

def fetch_pmc_xml(pmcid):
    """
    Fetch full-text XML from PubMed Central
    Tries multiple methods: OAI-PMH and E-utilities
    
    Args:
        pmcid: PubMed Central ID (e.g., 'PMC1234567' or just '1234567')
    
    Returns:
        XML content as string
    """
    # Clean PMCID - remove 'PMC' prefix if present for numeric ID
    numeric_id = pmcid[3:] if pmcid.startswith('PMC') else pmcid
    
    # Method 1: Try OAI-PMH (full JATS XML)
    print(f"  Trying OAI-PMH for PMC{numeric_id}...")
    try:
        base_url = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
        params = {
            'verb': 'GetRecord',
            'identifier': f'oai:pubmedcentral.nih.gov:{numeric_id}',
            'metadataPrefix': 'pmc'
        }
        
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        # Check if we got an error in the XML response
        if 'error' in response.text.lower() and 'idDoesNotExist' in response.text:
            print(f"  ✗ OAI-PMH: Article not found")
        else:
            print(f"  ✓ OAI-PMH: Success")
            return response.text
            
    except requests.exceptions.RequestException as e:
        print(f"  ✗ OAI-PMH failed: {e}")
    
    # Method 2: Try E-utilities efetch (alternative format)
    print(f"  Trying E-utilities for PMC{numeric_id}...")
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
            print(f"  ✓ E-utilities: Success")
            return response.text
        else:
            print(f"  ✗ E-utilities: Empty response")
            
    except requests.exceptions.RequestException as e:
        print(f"  ✗ E-utilities failed: {e}")
    
    print(f"  ✗ All methods failed to fetch PMC XML")
    return None

def extract_jats_article_type(xml_string):
    """
    Extract JATS article-type attribute from PMC XML
    
    Returns:
        article-type string or None
    """
    try:
        root = ET.fromstring(xml_string)
        
        # PMC XML has namespaces, need to handle them
        # The structure is: OAI-PMH > GetRecord > record > metadata > article
        
        # Method 1: Search for any element with tag ending in 'article' that has article-type attribute
        for elem in root.iter():
            tag_name = elem.tag
            # Remove namespace if present
            if '}' in tag_name:
                tag_name = tag_name.split('}')[1]
            
            if tag_name == 'article':
                article_type = elem.get('article-type')
                if article_type:
                    return article_type
        
        # Method 2: Try with namespace awareness
        # Common JATS namespaces
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
        print(f"Error extracting JATS article-type: {e}")
        return None

def debug_pmc_xml_structure(xml_string):
    """
    Debug function to inspect PMC XML structure
    Shows the first few levels of XML to help identify issues
    """
    try:
        root = ET.fromstring(xml_string)
        print("\n  [DEBUG] PMC XML Structure:")
        
        # Show first 3 levels
        def show_tree(elem, level=0, max_level=3):
            if level > max_level:
                return
            
            tag = elem.tag
            if '}' in tag:
                tag = tag.split('}')[1]
            
            attrs = elem.attrib
            attr_str = ""
            if attrs:
                attr_str = " [" + ", ".join([f"{k}='{v}'" for k, v in attrs.items()]) + "]"
            
            print("  " * level + f"├─ {tag}{attr_str}")
            
            for child in list(elem)[:5]:  # Show first 5 children only
                show_tree(child, level + 1, max_level)
        
        show_tree(root)
        print()
        
    except Exception as e:
        print(f"  [DEBUG] Error inspecting XML: {e}")


def get_article_title(xml_string):
    """
    Extract article title from PubMed XML
    """
    try:
        root = ET.fromstring(xml_string)
        title_elem = root.find('.//ArticleTitle')
        if title_elem is not None:
            return title_elem.text
        return "Title not found"
    except Exception as e:
        return "Error extracting title"

def pretty_print_xml(xml_string):
    """
    Pretty print XML string with proper indentation
    """
    try:
        dom = minidom.parseString(xml_string)
        return dom.toprettyxml(indent="  ")
    except Exception as e:
        print(f"Error formatting XML: {e}")
        return xml_string

def save_xml_to_file(xml_content, filename):
    """
    Save XML content to a file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"  ✓ Saved to {filename}")
    except Exception as e:
        print(f"  ✗ Error saving file: {e}")

# Main execution
if __name__ == "__main__":
    # Prompt user for PMID
    print("=" * 70)
    print("PubMed Article Type Extractor")
    print("=" * 70)
    print()
    
    pmid = input("Enter PMID (e.g., 38322404): ").strip()
    
    # Validate input
    if not pmid:
        print("Error: PMID cannot be empty")
        exit(1)
    
    # Remove any non-numeric characters
    pmid = ''.join(filter(str.isdigit, pmid))
    
    if not pmid:
        print("Error: Invalid PMID format")
        exit(1)
    
    print()
    print("=" * 70)
    print(f"FETCHING ARTICLE METADATA FOR PMID: {pmid}")
    print("=" * 70)
    print()
    
    # ===== STEP 1: Fetch PubMed XML =====
    print("STEP 1: Fetching PubMed bibliographic record...")
    pubmed_xml = fetch_pubmed_xml(pmid)
    
    if not pubmed_xml:
        print("Failed to fetch PubMed XML. Exiting.")
        exit(1)
    
    # Save PubMed XML
    pubmed_filename = f"pubmed_{pmid}.xml"
    formatted_pubmed_xml = pretty_print_xml(pubmed_xml)
    save_xml_to_file(formatted_pubmed_xml, pubmed_filename)
    
    # Get article title
    title = get_article_title(pubmed_xml)
    print(f"\nArticle Title: {title[:100]}...")
    print()
    
    # ===== STEP 2: Extract PublicationType from PubMed XML =====
    print("-" * 70)
    print("STEP 2: Extracting PublicationType (PubMed controlled vocabulary)")
    print("-" * 70)
    
    pub_types = extract_publication_types(pubmed_xml)
    
    if pub_types:
        print(f"\nFound {len(pub_types)} publication type(s):")
        for i, pt in enumerate(pub_types, 1):
            print(f"  {i}. {pt['type']}")
            if pt['ui']:
                print(f"     UI: {pt['ui']}")
    else:
        print("No publication types found.")
    
    print()
    
    # ===== STEP 3: Check for PMC version =====
    print("-" * 70)
    print("STEP 3: Checking for PubMed Central (PMC) version...")
    print("-" * 70)
    
    pmcid = get_pmcid_from_pubmed_xml(pubmed_xml)
    jats_type = None  # Initialize to avoid NameError later
    
    if pmcid:
        print(f"\n✓ Article is available in PMC: {pmcid}")
        print()
        
        # ===== STEP 4: Fetch PMC XML =====
        print("STEP 4: Fetching PMC full-text XML...")
        pmc_xml = fetch_pmc_xml(pmcid)
        
        if pmc_xml:
            # Save PMC XML
            pmc_filename = f"pmc_{pmcid}.xml"
            formatted_pmc_xml = pretty_print_xml(pmc_xml)
            save_xml_to_file(formatted_pmc_xml, pmc_filename)
            
            # ===== STEP 5: Extract JATS article-type =====
            print()
            print("-" * 70)
            print("STEP 5: Extracting JATS article-type attribute")
            print("-" * 70)
            
            jats_type = extract_jats_article_type(pmc_xml)
            
            if jats_type:
                print(f"\n✓ JATS article-type: '{jats_type}'")
                print(f"\n  Reference: https://jats.nlm.nih.gov/publishing/tag-library/1.1/attribute/article-type.html")
            else:
                print("\n✗ Could not extract JATS article-type attribute")
                print("  Debugging XML structure...")
                debug_pmc_xml_structure(pmc_xml)
        else:
            print("\n  ✗ Failed to fetch PMC XML")
            print("\n  Possible reasons:")
            print("    • Article may not be open access yet (embargo period)")
            print("    • PMC processing may still be in progress")
            print("    • Network/API issues")
            print("    • PMCID may be incorrect")
            print(f"\n  Try checking manually: https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/")
    else:
        print("\n✗ Article is not available in PubMed Central")
        print("  (JATS article-type only available for PMC articles)")
    
    # ===== SUMMARY =====
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nPMID: {pmid}")
    print(f"Title: {title[:80]}...")
    print()
    print("PubMed PublicationType(s):")
    if pub_types:
        for pt in pub_types:
            print(f"  • {pt['type']}")
    else:
        print("  (none found)")
    
    print()
    if pmcid and jats_type:
        print(f"PMC ID: {pmcid}")
        print(f"JATS article-type: '{jats_type}'")
    elif pmcid:
        print(f"PMC ID: {pmcid}")
        print("JATS article-type: (not extracted)")
    else:
        print("PMC: Not available")
        print("JATS article-type: N/A")
    
    print()
    print("=" * 70)
