import argparse
import logging
import pathlib
import pkg_resources
import shutil
import subprocess
import urllib.request
import zipfile

import ltu


logger = logging.getLogger(__name__)


_CONTAINER_IMAGE = "ltu-languagetool"


_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"


_NGRAMS = {
    "en": "https://languagetool.org/download/ngram-data/ngrams-en-20150817.zip",
}


def download_ngrams(language):
    url = _NGRAMS[language]
    zip_name = url.split("/")[-1]
    cache_path = pathlib.Path(ltu.dirs.user_cache_dir)
    cache_path.mkdir(exist_ok=True, parents=True)
    zip_path = cache_path / zip_name
    if not zip_path.exists():
        logger.info("Downloading %s to %s", url, zip_path)
        request = urllib.request.Request(
            url,
            headers={
                # for some reason, the Python user agent is rejected. But anything else I tried, including curl, worked.
                "User-Agent": _USER_AGENT,
            },
        )

        with urllib.request.urlopen(request) as d:
            with open(zip_path, "wb") as o:
                shutil.copyfileobj(d, o)

    ngrams_path = cache_path / language
    if ngrams_path.exists():
        return

    logging.info("Unzipping %s", zip_path)
    with zipfile.ZipFile(zip_path, "r") as zip:
        zip.extractall(cache_path)


def build_container():
    container_dir = pathlib.Path(pkg_resources.resource_filename(__name__, "foo")).parent.parent / "third-party" / "silvio-docker-languagetool"

    print("if prompted, select the docker.io image with your cursors and press enter")
    subprocess.run(["podman", "build", "--build-arg", "VERSION=5.9", "-t", _CONTAINER_IMAGE, container_dir], check=True)


def run_container_server():
    ngrams_path = pathlib.Path(ltu.dirs.user_cache_dir).absolute()
    subprocess.run(["podman", "run", "--rm", "-it", "-p", "8010:8010", "-v", f"{ngrams_path}:/ngrams", _CONTAINER_IMAGE], check=True)


def run_server_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ngrams", action="append")
    args = parser.parse_args()
    for ngram in args.ngrams or []:
        download_ngrams(ngram)
    build_container()
    run_container_server()
