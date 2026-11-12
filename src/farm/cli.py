"""Command-line entry point: `farm <group> <command>`. User-facing messages are in French."""

import typer
from dotenv import load_dotenv
from pydantic import ValidationError

from farm.core import config
from farm.core.jobs import JobStatus
from farm.core.storage import JobNotFound, JobStore

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


job_app = typer.Typer(help="Jobs : une fiche de suivi par vidéo.", no_args_is_help=True)
app.add_typer(job_app, name="job")

STATUS_HELP = "Statut : " + ", ".join(s.value for s in JobStatus)


def _job_line(job) -> str:
    cost = f"{job.cost_usd:.2f} $" if job.costs else "-"
    series = job.series or "-"
    return f"{job.id}  {job.status.value:<16} {series:<12} {cost:>8}  {job.idea[:50]}"


@job_app.command("new")
def job_new(
    channel: str = typer.Argument(..., help="Id de la chaîne."),
    series: str = typer.Option(None, "--series", "-s", help="Série récurrente, ex. hi_there."),
    idea: str = typer.Option("", "--idea", "-i", help="Idée de départ en une phrase."),
    language: str = typer.Option(None, "--lang", help="fr ou en."),
) -> None:
    """Crée un job au statut idea, avec son dossier jobs/<id>/inbox/."""
    config.load_channel(channel)  # fails loudly on an unknown or invalid channel
    if language not in (None, "fr", "en"):
        typer.secho("✗ --lang doit valoir fr ou en", fg="red")
        raise typer.Exit(1)
    store = JobStore()
    job = store.create(channel, series=series, idea=idea, language=language)
    typer.secho(f"✓ job {job.id} créé", fg="green")
    typer.echo(f"  dossier de dépôt : {store.inbox_dir(job.id)}")


@job_app.command("list")
def job_list(
    channel: str = typer.Option(None, "--channel", "-c"),
    status: str = typer.Option(None, "--status", help=STATUS_HELP),
    limit: int = typer.Option(20, "--limit", "-n"),
) -> None:
    """Liste les jobs, du plus récent au plus ancien."""
    if status and status not in JobStatus._value2member_map_:
        typer.secho(f"✗ statut inconnu : {status}. {STATUS_HELP}", fg="red")
        raise typer.Exit(1)
    jobs = JobStore().list(channel=channel, status=status, limit=limit)
    if not jobs:
        typer.echo("Aucun job.")
        return
    for job in jobs:
        typer.echo(_job_line(job))


@job_app.command("show")
def job_show(job_id: str) -> None:
    """Affiche la fiche complète d'un job."""
    try:
        job = JobStore().get(job_id)
    except (JobNotFound, ValueError):
        typer.secho(f"✗ job introuvable : {job_id}", fg="red")
        raise typer.Exit(1)
    typer.echo(job.model_dump_json(indent=2))


@job_app.command("status")
def job_status(
    job_id: str,
    new_status: str = typer.Argument(..., help=STATUS_HELP),
    note: str = typer.Option("", "--note", help="Motif, ex. raison d'un rejet."),
    force: bool = typer.Option(False, "--force", help="Autorise un passage hors du circuit normal."),
) -> None:
    """Change le statut d'un job (le passage est vérifié et tracé dans l'historique)."""
    store = JobStore()
    try:
        job = store.get(job_id)
        job.transition(new_status, note=note, force=force)
    except (JobNotFound, ValueError) as e:
        typer.secho(f"✗ {e}", fg="red")
        raise typer.Exit(1)
    store.save(job)
    typer.secho(f"✓ {job.id} → {job.status.value}", fg="green")


if __name__ == "__main__":
    app()
