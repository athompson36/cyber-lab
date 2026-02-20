"""Map manager commands — regions, tile estimate, SD/tile structure validation."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

# Repo root so we can import scripts
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

app = typer.Typer(no_args_is_help=True)
console = Console()


def _wizard_list_regions():
    from scripts.map_wizard import wizard_list_regions
    return wizard_list_regions()


def _wizard_estimate(region_slug: str, min_zoom: int, max_zoom: int):
    from scripts.map_wizard import wizard_estimate
    return wizard_estimate(region_slug, min_zoom, max_zoom)


def _validate_output_structure(path: Path):
    from scripts.map_wizard import validate_output_structure
    return validate_output_structure(path)


def _validate_tile_structure(path: Path):
    from scripts.sd_validator import validate_tile_structure
    return validate_tile_structure(path)


@app.command("list")
def map_list() -> None:
    """List predefined regions (continents, countries, states) for tile download."""
    try:
        out = _wizard_list_regions()
    except Exception as e:
        console.print(f"[red]Failed to load regions: {e}[/red]")
        raise typer.Exit(1)

    grouped = out.get("grouped", {})
    if not any(grouped.values()):
        console.print("[yellow]No regions found in regions/regions.json[/yellow]")
        return

    console.print("[bold]Regions (T-Deck / Meshtastic compatible)[/bold]\n")
    for cat in ("continent", "country", "state", "region", "province"):
        items = grouped.get(cat, [])
        if not items:
            continue
        table = Table(title=cat.upper(), show_header=True)
        table.add_column("Slug", style="cyan")
        table.add_column("Name")
        table.add_column("Country", style="dim")
        for r in items:
            table.add_row(r.get("slug", ""), r.get("name", ""), r.get("country", "") or "—")
        console.print(table)
        console.print()


@app.command("estimate")
def map_estimate(
    region: str = typer.Argument(..., help="Region slug (e.g. california, usa)"),
    min_zoom: int = typer.Option(8, "--min-zoom", "-z", help="Minimum zoom level"),
    max_zoom: int = typer.Option(12, "--max-zoom", "-Z", help="Maximum zoom level"),
) -> None:
    """Estimate tile count and size for a region and zoom range."""
    try:
        res = _wizard_estimate(region, min_zoom, max_zoom)
    except Exception as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    if not res:
        console.print(f"[red]Unknown region: {region}[/red]")
        raise typer.Exit(1)

    table = Table(title=f"Estimate — {res['region_slug']} (zoom {res['min_zoom']}-{res['max_zoom']})")
    table.add_column("Metric", style="bold")
    table.add_column("Value")
    table.add_row("Tile count", f"{res['tile_count']:,}")
    table.add_row("Estimated size", f"{res['estimated_mb']} MB ({res['estimated_gb']} GB)")
    table.add_row("Fits 16GB SD", "Yes" if res["sd_fits"].get("16GB") else "No")
    table.add_row("Fits 32GB SD", "Yes" if res["sd_fits"].get("32GB") else "No")
    table.add_row("Fits 64GB SD", "Yes" if res["sd_fits"].get("64GB") else "No")
    table.add_row("Fits 128GB SD", "Yes" if res["sd_fits"].get("128GB") else "No")
    console.print(table)


@app.command("validate")
def map_validate(
    path: str = typer.Argument("tiles", help="Path to tile folder (metadata.json + {z}/{x}/{y}.png)"),
) -> None:
    """Validate T-Deck tile folder structure (metadata.json, zoom dirs, PNG tiles)."""
    p = Path(path).resolve()
    try:
        res = _validate_output_structure(p)
    except Exception as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    if res.get("valid"):
        console.print("[green]Valid[/green] — tile structure OK")
    else:
        console.print("[red]Invalid[/red]")
        for e in res.get("errors", []):
            console.print(f"  [red]•[/red] {e}")
        raise typer.Exit(1)


@app.command("sd-validate")
def map_sd_validate(
    path: str = typer.Argument("tiles", help="Path to tile root to validate (metadata + zoom/x/y.png)"),
) -> None:
    """Validate tile structure with stats (zoom levels, tile count)."""
    p = Path(path).resolve()
    try:
        res = _validate_tile_structure(p)
    except Exception as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    if res.get("valid"):
        console.print("[green]Valid[/green]")
    else:
        console.print("[red]Invalid[/red]")
        for e in res.get("errors", []):
            console.print(f"  [red]•[/red] {e}")
    for w in res.get("warnings", []):
        console.print(f"  [yellow]⚠[/yellow] {w}")
    stats = res.get("stats", {})
    if stats:
        table = Table(show_header=False)
        table.add_column("Stat", style="bold")
        table.add_column("Value")
        table.add_row("Zoom levels", str(stats.get("zoom_levels", [])))
        table.add_row("Tile count", str(stats.get("tile_count", 0)))
        table.add_row("metadata.json", "Yes" if stats.get("has_metadata") else "No")
        console.print(table)
    if not res.get("valid"):
        raise typer.Exit(1)
