import os
import re
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
from difflib import unified_diff

def refine_page_links(page_info: dict, console: Console, graph_dir: str):
    """
    Interactively refine links for a given page.
    
    Args:
        page_info (dict): Information about the page to refine
        console (Console): Rich console for output
        graph_dir (str): Path to the Logseq graph directory
    """
    # Display page content
    console.print(Panel(
        Syntax(page_info['content'], "markdown", theme="monokai"),
        title=f"Page: {page_info['title']}"
    ))
    
    # Process backlinks
    for backlink in page_info['backlinks']:
        # Find the backlink file
        backlink_file = find_backlink_file(backlink, graph_dir)
        if not backlink_file:
            console.print(f"[yellow]Could not find file for backlink: {backlink}[/]")
            continue
        
        # Read backlink file content
        with open(backlink_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Generate refined content by removing links to current page
        refined_content = remove_page_links(original_content, page_info['title'])
        
        # Show diff
        diff = list(unified_diff(
            original_content.splitlines(),
            refined_content.splitlines(),
            fromfile="Original",
            tofile="Refined",
            lineterm=""
        ))
        
        console.print("\n[bold]Proposed Link Refinement:[/]")
        console.print(f"Backlink Page: {backlink}")
        
        # Colorize diff
        for line in diff:
            if line.startswith('-'):
                console.print(f"[red]{line}[/]")
            elif line.startswith('+'):
                console.print(f"[green]{line}[/]")
            else:
                console.print(line)
        
        # Ask for confirmation
        if console.input("[bold yellow]Apply this refinement? (y/N): [/]").lower().strip() == 'y':
            with open(backlink_file, 'w', encoding='utf-8') as f:
                f.write(refined_content)
            console.print("[green]Refinement applied![/]")
        else:
            console.print("[yellow]Refinement skipped.[/]")

def find_backlink_file(backlink: str, graph_dir: str) -> str:
    """
    Find the file for a given backlink.
    
    Args:
        backlink (str): Backlink page name
        graph_dir (str): Path to the Logseq graph directory
    
    Returns:
        str: Path to the backlink file, or None if not found
    """
    # Search in pages and journals directories
    for directory in ['pages', 'journals']:
        filepath = os.path.join(graph_dir, directory, f"{backlink}.md")
        if os.path.exists(filepath):
            return filepath
    return None

def remove_page_links(content: str, page_title: str) -> str:
    """
    Remove links to a specific page from content.
    
    Args:
        content (str): Original file content
        page_title (str): Page title to remove links for
    
    Returns:
        str: Refined content with links removed
    """
    # Regex to match [[page_title]] or [[page_title/subpage]] or [[page_title/subpage/nested]]
    link_pattern = re.compile(r'\[\[' + re.escape(page_title) + r'(/[^\]]*)?]]')
    
    # Replace links with the page title and its nested path
    return link_pattern.sub(lambda m: m.group(0)[2:-2], content)
