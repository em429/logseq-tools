import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path

from .link_parser import LogseqLinkParser
from .refiner import GraphRefiner

console = Console()

@click.command()
@click.option('--pages-dir', default='.', help='Directory containing Logseq markdown pages')
@click.option('--max-backlinks', default=5, help='Maximum number of backlinks to consider for refinement')
@click.option('--max-content-lines', default=3, help='Maximum content lines for a page to be considered for refinement')
def main(pages_dir: str, max_backlinks: int, max_content_lines: int):
    """Refine Logseq graph by removing unnecessary backlinks."""
    pages_path = Path(pages_dir)
    
    console.print(Panel.fit("Logseq Graph Refiner", title="🔍 Scanning Pages"))
    
    # Scan and index links
    link_map = LogseqLinkParser.scan_pages(pages_path)
    
    # Initialize refiner
    refiner = GraphRefiner(
        link_map, 
        max_backlinks=max_backlinks, 
        max_content_lines=max_content_lines
    )
    
    # Identify refinement candidates
    candidates = refiner.identify_refinement_candidates()
    
    if not candidates:
        console.print("[green]No pages found that meet refinement criteria.[/green]")
        return
    
    console.print(f"[yellow]Found {len(candidates)} pages for potential refinement.[/yellow]")
    
    # Interactive refinement
    for candidate in candidates:
        backlinks = refiner.get_page_backlinks(candidate)
        
        console.print(Panel(
            f"Candidate Page: [bold]{candidate}[/bold]\n"
            f"Backlinks: {len(backlinks)}",
            title="🎯 Refinement Target"
        ))
        
        for source_page in backlinks:
            original_content = refiner.get_page_content(source_page)
            modified_content = refiner.remove_link_from_page(source_page, candidate)
            
            console.print("\n[blue]Original Content:[/blue]")
            console.print(original_content)
            
            console.print("\n[green]Modified Content:[/green]")
            console.print(modified_content)
            
            confirm = click.confirm("Apply this change?")
            if confirm:
                # TODO: Implement actual file writing logic
                console.print(f"[green]Removed link to {candidate} from {source_page}[/green]")
            else:
                console.print(f"[yellow]Skipped removing link to {candidate} from {source_page}[/yellow]")

if __name__ == '__main__':
    main()
