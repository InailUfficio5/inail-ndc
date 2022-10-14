import json
import logging
from pathlib import Path
from sys import argv

import pandas as pd
from pyld import jsonld
from rdflib import Graph  # pip install rdflib pyld

# EXAMPLE: python create_csv_json.py <nome-file>
log = logging.getLogger(__name__)
MIME_JSONLD = "application/ld+json"


def save_to_json(frame, output_path_json):
    with open(output_path_json, "w") as fh:
        json.dump(frame, indent=2, fp=fh)


# Return the value of the father
def get_father(x):
    return x[list(x)[-1]]


def save_to_csv(framed_data, context, output_path):
    # Generate CSV.
    df = pd.DataFrame(framed_data["@graph"])
    # df.drop(['url', '@type'], axis=1, inplace=True)
    df.drop(['@type'], axis=1, inplace=True)
    if "parent" in df:
        df["parent"] = df["parent"] \
            .transform(lambda x: get_father(x) if pd.isna(x) is False else x)

    df.to_csv(output_path, sep=',', index=False)
    # print(df.to_string())


def framer(vocab_path):
    # frame_path = Path(vocab_path).parent.joinpath("context-short.ld.json")
    # Get the json-ld frame path
    frame_path_list = list(Path(vocab_path).parent.glob('*.jsonld'))

    if not frame_path_list:
        log.error(f"Frame file not present in: {Path(vocab_path).parent}")
        exit(1)

    frame_path = frame_path_list[0]
    # Exit asap.
    if not Path(frame_path).is_file():
        log.error(f"File not present: {frame_path}")
        exit(1)

    # ignore format different from .ttl
    if not vocab_path.endswith('.ttl'):
        return

    output_path_csv = vocab_path.replace(".ttl", ".csv")
    # output_path_json = vocab_path.replace(".ttl", ".json")
    rdf_graph = Graph()
    rdf_graph.parse(vocab_path, format='ttl')
    rdf_tree = json.loads(rdf_graph.serialize(format=MIME_JSONLD))
    context = json.loads(frame_path.read_text())

    # Define a projection
    frame_json = jsonld.frame(rdf_tree, frame=context)
    # save_to_json(definizione_amministrativa_json)
    save_to_csv(frame_json, context, output_path_csv)
    # save_to_json(rdf_tree, output_path_json)


if __name__ == "__main__":

    files = argv[1:]
    for f in files:
        framer(f)
