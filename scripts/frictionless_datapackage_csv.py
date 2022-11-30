# Source: https://github.com/ioggstream/dati-eu-authority-tables

import json
import logging
import os
from multiprocessing import Pool
from pathlib import Path

import click
import pandas as pd
import yaml
from frictionless import Resource
from pyld import jsonld
from rdflib.graph import Graph
from rdflib.plugins.serializers.jsonld import from_rdf

log = logging.getLogger(__name__)
VOCAB_PATH = "./assets/controlled-vocabularies/"
FRAME_PATH = "./assets/controlled-vocabularies/frame-short.yamlld"
MIME_JSONLD = "application/ld+json"


# Return the value of the father
def get_father(x):
    return x[list(x)[-1]]


# Get vocabularies list
def get_vocabularies(vocab_directory):

    for root, dirs, files in os.walk(vocab_directory):
        for file in files:
            if file.endswith('.ttl'):
                # print(os.path.join(root, file))
                # print(file)
                yield "", Path(os.path.join(root, file))


def to_jsonld(url, src_file):
    dest_file = src_file.with_suffix(".jsonld")
    g = Graph()
    g.parse(src_file.as_posix())
    g.serialize(format="json-ld", destination=dest_file.as_posix())
    return url, dest_file


def to_json(url, src_file):
    g = Graph()
    g.parse(src_file.with_suffix(".ttl").as_posix())
    data = from_rdf(g)
    frame = yaml.safe_load(Path(FRAME_PATH).read_text())
    frame.pop("_meta")
    json_data = jsonld.frame(data, frame)
    context, graph = json_data["@context"], json_data["@graph"]
    ## graph.drop(columns=["@type"], inplace=True)

    dest_json = src_file.with_suffix(".json")
    dest_json.write_text(json.dumps(graph, indent=2))
    ## df.to_json(dest_json, indent=2)
    # out = json.loads(graph)
    # df = pd.json_normalize(out, meta=[])
    # df["@type"] = df["@type"][-1]
    # graph = df.reset_index().to_json(orient='record')
    #print(graph)
    ### Uncomment to write datapackage
    #write_datapackage(graph, context, src_file)
    return url, dest_json


def write_datapackage(graph, context, dest_file):
    resource = Resource(data=graph)
    # print(resource)
    resource.infer()
    resource_dict = resource.to_dict()
    resource_dict.update(
        {"name": dest_file.stem, "path": dest_file.with_suffix(".csv").name}
    )
    resource_dict.pop("data")
    datapackage_yaml = Path(dest_file.parent / "datapackage.yaml")
    if datapackage_yaml.exists():
        datapackage = yaml.safe_load(datapackage_yaml.read_text())
        for r in datapackage["resources"]:
            if r["name"] == dest_file.stem:
                r.update(resource_dict)
                break
        else:
            datapackage["resources"].append(resource_dict)
    else:
        datapackage = {
            "name": dest_file.stem,
            "resources": [resource_dict],
        }
    datapackage["resources"][-1]["schema"]["x-jsonld-context"] = context
    if gtype := graph[0].get("@type"):
        datapackage["resources"][-1]["schema"]["x-jsonld-type"] = gtype
    datapackage_yaml.write_text(yaml.safe_dump(datapackage))
    # print("ho scritto: " +datapackage_yaml)


def to_csv(url, src_file):
    # rdf_graph = Graph()
    # rdf_graph.parse(src_file, format='ttl')
    # out = json.loads(rdf_graph.serialize(format=MIME_JSONLD))
    out = json.loads(src_file.read_text())
    dest_csv = src_file.with_suffix(".csv")

    df = pd.json_normalize(out, meta=[])
    df.drop(columns=["@type"], inplace=True)
    if "parent" in df:
        df["parent"] = df["parent"] \
            .transform(lambda x: get_father(x) if pd.isna(x) is False else x)
    df.to_csv(dest_csv, index=False, sep=",", header=True, quotechar='"')

    # g = Graph()
    # g.parse(src_file.with_suffix(".ttl").as_posix())
    # data = from_rdf(g)
    # frame = yaml.safe_load(Path(FRAME_PATH).read_text())
    # frame.pop("_meta")
    # json_data = jsonld.frame(data, frame)
    # df = pd.json_normalize(json_data, meta=[])
    # df.drop(columns=["@type"], inplace=True)
    # if "parent" in df:
    #     df["parent"] = df["parent"] \
    #         .transform(lambda x: get_father(x) if pd.isna(x) is False else x)
    # context, graph = json_data["@context"], json_data["@graph"]
    # dest_csv = src_file.with_suffix(".csv")
    # df.to_csv(dest_csv, index=False, sep=",", header=True, quotechar='"')

    # write_datapackage(graph, context, src_file)

    return url, src_file.with_suffix(".csv")


def pipeline(*args):
    for f in (
        to_json,
        to_csv,
    ):
        log.warning("Running %s(%s)", f.__name__, args)
        args = f(*args)
        if args is None:
            return
        log.warning("Result %s", args)


@click.command()
@click.option("--forks", default=1, help="processes to spawn")
@click.option("--needle", default="", help="tables to get")
def main(forks, needle):
    vocabs = get_vocabularies(VOCAB_PATH)

    with Pool(processes=forks) as workers:
        workers \
            .starmap(pipeline, ((x, y) for x, y in vocabs if needle in x))


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
