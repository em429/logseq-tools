from typing import Dict, Set, List
from pathlib import Path
import re

class GraphRefiner:
    def __init__(self, link_map: Dict[str, Dict[str, Set[str]]], 
                 max_backlinks: int = 5, 
                 max_content_lines: int = 3):
        """
        Initialize graph refiner with link map and refinement criteria.
        
        :param link_map: Comprehensive map of pages and their links
        :param max_backlinks: Maximum number of backlinks to consider for refinement
        :param max_content_lines: Maximum number of content lines for a page to be considered for refinement
        """
        self.link_map = link_map
        self.max_backlinks = max_backlinks
        self.max_content_lines = max_content_lines
    
    def identify_refinement_candidates(self) -> List[str]:
        """
        Identify pages that meet refinement criteria.
        
        Criteria:
        1. More than max_backlinks
        2. Content is minimal (less than max_content_lines)
        """
        candidates = []
        
        for page, data in self.link_map.items():
            backlink_count = len(data['backlinks'])
            content_lines = len(data['content'].split('\n')) if data['content'] else 0
            
            if (backlink_count > self.max_backlinks and 
                content_lines <= self.max_content_lines):
                candidates.append(page)
        
        return candidates
    
    def get_page_backlinks(self, page: str) -> List[str]:
        """Get all pages that link to the specified page."""
        return list(self.link_map.get(page, {}).get('backlinks', []))
    
    def get_page_content(self, page: str) -> str:
        """Get content of a specific page."""
        return self.link_map.get(page, {}).get('content', '')
    
    def remove_link_from_page(self, source_page: str, target_page: str) -> str:
        """
        Remove a specific link from a page's content.
        
        :param source_page: Page containing the link
        :param target_page: Page to be unlinked
        :return: Modified page content
        """
        content = self.link_map[source_page]['content']
        link_pattern = re.compile(rf'\[\[{target_page}\]\]')
        return link_pattern.sub(target_page, content)
