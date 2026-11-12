"""Command-line entry point: `farm <group> <command>`. User-facing messages are in French."""

import typer
from dotenv import load_dotenv
from pydantic import ValidationError

from farm.core import config

app = typer.Typer(help="Moteur d'agents IA de production vidéo.", no_args_is_help=True)
config_app = typer.Typer(help="Configs de chaîne et règles.", no_args_is_help=True)
app.add_typer(config_app, name="config")


@app.callback()
def _init() -> None:
    load_dotenv(config.project_root() / ".env")


@config_app.command("check")
def config_check(channel: str = typer.Argument(None, help="Id de la chaîne (toutes si vide).")) -> None:
    """Valide les configs de chaîne et les fichiers de règles."""
    ids = [channel] if channel else config.list_channels()
    failed = False
    for cid in ids:
        try:
            cfg = config.load_channel(cid)
            problems = config.check_channel(cfg)
        except (ValidationError, ValueError, FileNotFoundError) as e:
            typer.secho(f"✗ {cid} : config invalide\n{e}", fg="red")
            failed = True
            continue
        if problems:
            typer.secho(f"⚠ {cid} : {len(problems)} point(s) à régler", fg="yellow")
            for p in problems:
                typer.echo(f"  - {p}")
        else:
            typer.secho(f"✓ {cid}", fg="green")
    raise typer.Exit(1 if failed else 0)


@config_app.command("show")
def config_show(channel: str) -> None:
    """Affiche la config d'une chaîne telle que le moteur la lit."""
    cfg = config.load_channel(channel)
    typer.echo(cfg.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
