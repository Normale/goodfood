"""Database setup script - Initialize PostgreSQL database with pgvector."""

import asyncio
import sys

from rich.console import Console
from rich.panel import Panel

from src.config.settings import settings

console = Console()


async def setup_database():
    """Set up the database with pgvector extension."""
    try:
        import asyncpg

        console.print(
            Panel(
                "[bold cyan]Setting up GoodFood database...[/bold cyan]",
                title="[bold cyan]Database Setup[/bold cyan]",
                border_style="cyan",
            )
        )

        # Parse database URL
        db_url = settings.database_url
        conn_params = {}

        if "@" in db_url:
            # Extract connection parameters
            parts = db_url.replace("postgresql://", "").split("@")
            user_pass = parts[0].split(":")
            host_db = parts[1].split("/")
            host_port = host_db[0].split(":")

            conn_params = {
                "user": user_pass[0],
                "password": user_pass[1] if len(user_pass) > 1 else "",
                "host": host_port[0],
                "port": int(host_port[1]) if len(host_port) > 1 else 5432,
                "database": host_db[1] if len(host_db) > 1 else "goodfood",
            }

        console.print(f"[cyan]Connecting to PostgreSQL at {conn_params['host']}...[/cyan]")

        # Connect to postgres database to create goodfood database
        conn = await asyncpg.connect(
            user=conn_params["user"],
            password=conn_params["password"],
            host=conn_params["host"],
            port=conn_params["port"],
            database="postgres",
        )

        # Check if database exists
        db_exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            conn_params["database"],
        )

        if not db_exists:
            console.print(f"[yellow]Creating database '{conn_params['database']}'...[/yellow]")
            await conn.execute(f'CREATE DATABASE {conn_params["database"]}')
            console.print(f"[green]✓ Database '{conn_params['database']}' created[/green]")
        else:
            console.print(f"[yellow]Database '{conn_params['database']}' already exists[/yellow]")

        await conn.close()

        # Connect to goodfood database to set up pgvector
        conn = await asyncpg.connect(
            user=conn_params["user"],
            password=conn_params["password"],
            host=conn_params["host"],
            port=conn_params["port"],
            database=conn_params["database"],
        )

        console.print("[cyan]Installing pgvector extension...[/cyan]")

        # Create pgvector extension
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

        console.print("[green]✓ pgvector extension installed[/green]")

        await conn.close()

        console.print(
            Panel(
                "[bold green]Database setup completed successfully![/bold green]\n\n"
                "[cyan]Next steps:[/cyan]\n"
                "1. Run migrations: alembic upgrade head\n"
                "2. Configure .env file with your settings\n"
                "3. Start using: python main.py demo",
                title="[bold green]✅ Success[/bold green]",
                border_style="green",
            )
        )

    except ImportError:
        console.print(
            Panel(
                "[bold red]Error: asyncpg not installed[/bold red]\n\n"
                "Install it with: pip install asyncpg\n"
                "Or: uv add asyncpg",
                title="[bold red]Missing Dependency[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except Exception as e:
        console.print(
            Panel(
                f"[bold red]Database setup failed:[/bold red]\n\n{str(e)}\n\n"
                "[cyan]Make sure PostgreSQL is running and accessible.[/cyan]",
                title="[bold red]❌ Error[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(setup_database())
