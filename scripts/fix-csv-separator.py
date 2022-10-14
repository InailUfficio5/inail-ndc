#
# Convert CSV separator to comma using pandas
#
import logging
from pathlib import Path
from sys import argv

import pandas as pd

log = logging.getLogger(__name__)


def has_valid_separator(f: Path):

    reader = pd.read_csv(f, sep=None, iterator=True, engine='python')
    df = pd.concat(reader)
    delimiter = reader._engine.data.dialect.delimiter

    if delimiter == ",":
        log.info(f"Valid CSV separator in {f.absolute().as_posix()}")
    else:
        log.error(f"Invalid CSV separator in {f.absolute().as_posix()}")
        log.error(f"Found '{delimiter}' instead of comma")
        df.to_csv(f, sep=',', index=False)
        exit(1)


if __name__ == "__main__":
    files = argv[1:]

    for f in files:
        if not f.lower().endswith(".csv"):
            continue
        f = Path(f)
        has_valid_separator(f)
