import os
from metaflow._vendor import click
from metaflow.cli import echo_always as echo

from .fast_bakery import read_metafile, BAKERY_METAFILE


@click.group()
def cli():
    pass


@cli.group(help="Commands related to Docker support.")
def docker():
    pass


@docker.group(help="Commands related to the Image Bakery local cache.")
def cache():
    pass


@cache.command(help="Clean the cached image tags")
def clean():
    try:
        os.remove(BAKERY_METAFILE)
        echo("Cache cleared.")
    except FileNotFoundError:
        echo("No cache found")
        pass


@cache.command(help="List the cached images")
def list():
    current_cache = read_metafile()

    if current_cache:
        echo("List of locally cached image tags:\n")

    for val in current_cache.values():
        packages = val["bakery_request"]["condaMatchspecs"]
        kind = val["kind"]
        base_image = (
            val["bakery_request"].get("baseImage", {}).get("imageReference", None)
        )

        echo(val["image"])
        echo("     image type: *%s*" % kind)
        if base_image:
            echo("     base image: *%s*" % base_image)
        echo("     packages requested: %s\n" % packages)

    if current_cache:
        echo(
            "In order to clear the cached images, you can use the commmand\n *docker cache clean*"
        )
