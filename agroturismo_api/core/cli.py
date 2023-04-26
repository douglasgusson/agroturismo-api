import typer
import uvicorn
from sqlmodel import Session

from ..models.admin_user import AdminUser
from ..models.user import User
from .db import create_db_and_tables, engine

cli = typer.Typer(name="Agrorturismo API")


@cli.command()
def run(
    port: int = 8000,
    host: str = "localhost",
    log_level: str = "info",
    reload: bool = True,
):  # pragma: no cover
    """Run the API server."""
    uvicorn.run(
        "agroturismo_api.main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@cli.command()
def create_super_admin_user(username: str, password: str):
    """Create user"""
    create_db_and_tables(engine)
    with Session(engine) as session:
        user = AdminUser(username=username, password=password, is_superuser=True)
        session.add(user)
        session.commit()
        session.refresh(user)
        typer.echo(f"created {username} user")
        return user
