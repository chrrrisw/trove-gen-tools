import argparse
from .aggregator import Aggregator


def main():
    # TODO: Multiple from_dbname

    parser = argparse.ArgumentParser()
    parser.add_argument("from_dbname", type=str)
    parser.add_argument("to_dbname", type=str)
    args = parser.parse_args()

    agg = Aggregator(args.from_dbname, args.to_dbname)


if __name__ == "__main__":
    main()
