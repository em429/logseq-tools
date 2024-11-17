import os
import re
from typing import Dict, List

def analyze_graph(pages_dir: str, journals_dir: str, min_content: int) -> Dict[str, Dict]:
    """
    Analyze Logseq graph pages and journals.
    
    Args:
        pages_dir (str): Path to pages directory
        journals_dir (str): Path to journals directory
        min_content (int): Minimum character count to consider a page non-empty
    
    Returns:
        Dict of page analysis information
    """
    graph_analysis = {}
    
    # Process pages and journals
    for directory in [pages_dir, journals_dir]:
        for filename in os.listdir(directory):
            if not filename.endswith('.md'):
                continue
            
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract page title from filename (without .md)
            page_title = os.path.splitext(filename)[0]
            
            # Find all backlinks to this page
            backlinks = find_backlinks(directory, page_title)
            
            graph_analysis[filepath] = {
                'title': page_title,
                'content': content,
                'is_empty': len(content.strip()) <= min_content,
                'backlinks': backlinks
            }
    
    return graph_analysis

def find_backlinks(directory: str, target_page: str) -> List[str]:
    """
    Find all pages that link to the target page.
    
    Args:
        directory (str): Directory to search for backlinks
        target_page (str): Page to find backlinks for
    
    Returns:
        List of pages that link to the target page
    """
    backlinks = []
    
    # Regex to match [[target_page]] or [[target_page/subpage]]
    link_pattern = re.compile(r'\[\[' + re.escape(target_page) + r'(/[^\]]*)?]]')
    
    for filename in os.listdir(directory):
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if this page links to the target page
        if link_pattern.search(content):
            backlinks.append(os.path.splitext(filename)[0])
    
    return backlinks
