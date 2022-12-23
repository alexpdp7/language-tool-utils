import argparse
import io
import subprocess

from ltu import client, html_annotations


def check_asciidoctor(f, language, asciidoctor_extra_args=["-a", "experimental"], endpoint="http://localhost:8010", level="picky", disabled_rules=["WHITESPACE_RULE"]):
    xhtml5 = subprocess.run(["asciidoctor", f, "-b", "xhtml5", "-o", "-"] + asciidoctor_extra_args, check=True, stdout=subprocess.PIPE).stdout
    annotations = html_annotations.annotate(io.StringIO(xhtml5.decode("utf-8")))
    return client.check(annotations, language, endpoint, level, disabled_rules)


def check_asciidoctor_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--language")
    parser.add_argument("--endpoint", default="http://localhost:8010")
    parser.add_argument("--level", default="picky")

    args=parser.parse_args()
    results = check_asciidoctor(args.file, args.language, endpoint=args.endpoint, level=args.level)
    for match in results["matches"]:
        context = match["context"]
        print(context["text"])
        print(" " * (context["offset"] - 1), "~" * context["length"])
        print(match["message"])
        print("_" * 80)
