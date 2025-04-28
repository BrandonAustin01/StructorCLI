# cli.py
import click

@click.command()
def hello():
    click.echo("Hello from CLI!")

if __name__ == "__main__":
    hello()
