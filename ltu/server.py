import argparse
import logging
import pathlib
import pkg_resources
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import ltu
from ltu.util import _


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
        logger.info("%s exists, done", ngrams_path)
        return

    logging.info("Unzipping %s", zip_path)
    with zipfile.ZipFile(zip_path, "r") as zip:
        zip.extractall(cache_path)

    logging.info("Extracted zip, truncating")
    with open(zip_path, "w"):
        # truncate the zip; keep it there to "mark" it has been downloaded and extracted
        pass

    logging.info("Done")


def build_container():
    container_dir = pathlib.Path(pkg_resources.resource_filename(__name__, "foo")).parent.parent / "third-party" / "silvio-docker-languagetool"

    print("if prompted, select the docker.io image with your cursors and press enter")
    subprocess.run(["podman", "build", "--build-arg", "VERSION=5.9", "-t", _CONTAINER_IMAGE, container_dir], check=True)


def run_container_server():
    ngrams_path = pathlib.Path(ltu.dirs.user_cache_dir).absolute()
    subprocess.run(["podman", "run", "--rm", "-it", "-p", "8010:8010", "-v", f"{ngrams_path}:/ngrams", "--security-opt", "label=disable", _CONTAINER_IMAGE], check=True)


def build_server_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ngrams", action="append")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    for ngram in args.ngrams or []:
        download_ngrams(ngram)
    build_container()


def install_server():
    systemd_path = pathlib.Path.home() / ".local" / "share" / "systemd" / "user"
    systemd_path.mkdir(parents=True, exist_ok=True)
    systemd_file = systemd_path / f"{ltu.APP_NAME}-server.service"
    server_cmd = pathlib.Path(sys.argv[0]).parent / "ltu-run-server"
    with open(systemd_file, "w", encoding="utf8") as f:
        f.write(_(f"""
            [Service]
            ExecStart={server_cmd}
            TimeoutStopSec=5

            [Install]
            WantedBy=default.target
        """))
    print(_(f"""
        Created {systemd_file}.

        $ systemctl --user [start|stop] language-tool-utils-server.service
        $ journalctl --user-unit language-tool-utils-server.service
        $ systemctl --user enable [--now] language-tool-utils-server.service
    """))
