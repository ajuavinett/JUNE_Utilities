#!/usr/bin/env python3
"""
Script to fetch PubMed article XML using NCBI E-utilities
"""

import requests
import xml.dom.minidom as minidom

def fetch_pubmed_xml(pmid):
    """
    Fetch XML data for a PubMed article using E-utilities
    
    Args:
        pmid: PubMed ID (PMID) as string or integer
    
    Returns:
        XML content as string
    """
    # E-utilities EFetch URL
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    # Parameters for the request
    params = {
        'db': 'pubmed',           # Database: PubMed
        'id': pmid,               # PubMed ID
        'retmode': 'xml',         # Return format: XML
        'rettype': 'abstract'     # Return type: abstract
    }
    
    try:
        # Make the request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise error for bad status codes
        
        return response.text
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

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
        print(f"XML saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

# Main execution
if __name__ == "__main__":
    # PubMed ID to fetch
    pmid = "38322404"
    
    print(f"Fetching XML for PMID: {pmid}")
    print("-" * 50)
    
    # Fetch the XML
    xml_data = fetch_pubmed_xml(pmid)
    
    if xml_data:
        # Pretty print the XML
        formatted_xml = pretty_print_xml(xml_data)
        
        # Print to console (first 2000 characters)
        print("XML Preview:")
        print(formatted_xml[:2000])
        print("\n[...truncated...]")
        
        # Save to file
        output_filename = f"pubmed_{pmid}.xml"
        save_xml_to_file(formatted_xml, output_filename)
        
        print(f"\nFull XML has been saved to: {output_filename}")
    else:
        print("Failed to fetch XML data")
