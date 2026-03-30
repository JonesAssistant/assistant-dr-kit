import typer

app = typer.Typer(help="assistant-dr-kit CLI")

@app.command()
def init():
    """Create a sample assistant-dr.yaml config."""
    ...

@app.command()
def bundle():
    """Build a DR bundle from assistant-dr.yaml."""
    ...

@app.command()
def generate_revive():
    """Generate a revive-assistant.sh script."""
    ...

if __name__ == "__main__":
    app()
