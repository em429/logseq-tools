import click
import os
from rich.console import Console
from rich.table import Table
from .page_analyzer import analyze_graph
from .page_refiner import refine_page_links

@click.command()
@click.argument('graph_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--min-content', default=0, help='Minimum character count to consider a page non-empty')
@click.option('--interactive/--no-interactive', default=True, help='Interactive refinement mode')
def main(graph_dir, min_content, interactive):
    """Refine Logseq graph by cleaning unnecessary links and empty pages."""
    console = Console()
    
    # Validate graph directory
    pages_dir = os.path.join(graph_dir, 'pages')
    journals_dir = os.path.join(graph_dir, 'journals')
    
    if not (os.path.exists(pages_dir) and os.path.exists(journals_dir)):
        console.print("[bold red]Error:[/] Invalid Logseq graph directory")
        return
    
    # Analyze graph
    graph_analysis = analyze_graph(pages_dir, journals_dir, min_content)
    
    # Sort pages by backlink count, descending
    pages_to_refine = sorted(
        graph_analysis.items(), 
        key=lambda x: len(x[1]['backlinks']), 
        reverse=True
    )
    
    console.print(f"[bold]Found {len(pages_to_refine)} pages to potentially refine[/]")
    
    # Interactive refinement
    for page_path, page_info in pages_to_refine:
        if not page_info['backlinks']:
            continue
        
        console.print(f"\n[bold]Refinement Target:[/] {page_info['title']}")
        console.print(f"Backlinks: {len(page_info['backlinks'])}")
        
        if interactive:
            refine_page_links(page_info, console, graph_dir)
        else:
            # Non-interactive mode: just print potential refinements
            console.print("Potential link refinements:")
            for backlink in page_info['backlinks']:
                console.print(f"- {backlink}")

if __name__ == '__main__':
    main()
