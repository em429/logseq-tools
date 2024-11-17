import os
import yaml
from typing import List, Dict, Optional

DEFAULT_CONFIG_PATH = os.path.expanduser('~/.logseq-refine-config.yaml')

class LogseqRefineConfig:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration for Logseq Graph Refiner
        
        :param config_path: Path to the configuration file, defaults to ~/.logseq-refine-config.yaml
        """
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """
        Load configuration from file, creating a default if not exists
        
        :return: Configuration dictionary
        """
        if not os.path.exists(self.config_path):
            # Create default configuration
            default_config = {
                'skip_pages': [],
                'skip_hierarchies': []
            }
            self._save_config(default_config)
            return default_config

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f) or {}

    def _save_config(self, config: Dict):
        """
        Save configuration to file
        
        :param config: Configuration dictionary to save
        """
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.safe_dump(config, f)

    def get_skip_pages(self) -> List[str]:
        """
        Get list of pages to skip
        
        :return: List of page names to skip
        """
        return self.config.get('skip_pages', [])

    def get_skip_hierarchies(self) -> List[str]:
        """
        Get list of hierarchies to skip
        
        :return: List of hierarchy prefixes to skip
        """
        return self.config.get('skip_hierarchies', [])

    def add_skip_page(self, page_name: str):
        """
        Add a page to the skip list
        
        :param page_name: Page name to skip
        """
        if page_name not in self.config.get('skip_pages', []):
            skip_pages = self.config.get('skip_pages', [])
            skip_pages.append(page_name)
            self.config['skip_pages'] = skip_pages
            self._save_config(self.config)

    def add_skip_hierarchy(self, hierarchy_prefix: str):
        """
        Add a hierarchy prefix to the skip list
        
        :param hierarchy_prefix: Hierarchy prefix to skip
        """
        if hierarchy_prefix not in self.config.get('skip_hierarchies', []):
            skip_hierarchies = self.config.get('skip_hierarchies', [])
            skip_hierarchies.append(hierarchy_prefix)
            self.config['skip_hierarchies'] = skip_hierarchies
            self._save_config(self.config)
