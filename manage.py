import typer
import os

app = typer.Typer()

@app.command()
def migrate():
    """Run Alembic migrations (like artisan migrate)"""
    os.system("alembic upgrade head")

if __name__ == "__main__":
    app()
