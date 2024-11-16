import re
from pathlib import Path
from typing import List, Dict, Set, Tuple

class LogseqLinkParser:
    LINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')
    
    @classmethod
    def find_all_links(cls, content: str) -> List[str]:
        """Find all Logseq-style links in a given text."""
        return [match.group(1) for match in cls.LINK_PATTERN.finditer(content)]
    
    @classmethod
    def remove_link(cls, content: str, link: str) -> str:
        """Remove a specific link from content."""
        return content.replace(f'[[{link}]]', link)
    
    @classmethod
    def scan_pages(cls, pages_dir: Path) -> Dict[str, Dict[str, Set[str]]]:
        """
        Scan all markdown files and build a comprehensive link map.
        
        Returns a dictionary where:
        - Keys are target pages
        - Values are dictionaries with:
          - 'backlinks': set of pages linking to this page
          - 'content': page content
        """
        link_map = {}
        
        for md_file in pages_dir.rglob('*.md'):
            content = md_file.read_text()
            page_name = md_file.stem
            
            # Find all links in this page
            links = cls.find_all_links(content)
            
            for link in links:
                # Normalize link (remove hierarchy if present)
                normalized_link = link.split('/')[-1]
                
                if normalized_link not in link_map:
                    link_map[normalized_link] = {
                        'backlinks': set(),
                        'content': ''
                    }
                
                link_map[normalized_link]['backlinks'].add(page_name)
            
            # Store page content
            link_map[page_name] = {
                'backlinks': link_map.get(page_name, {}).get('backlinks', set()),
                'content': content
            }
        
        return link_map
