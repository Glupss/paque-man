import sys
import argparse
from config import GameConfig
from engine import Engine


def main():

    parser = argparse.ArgumentParser(description="Launching PacMan")
    parser.add_argument(
        "config_file",
        type=str,
        help="Path to the file config.json",
    )

    args = parser.parse_args()

    if not args.config_file.endswith(".json"):
        print("[ERROR]: the config file must be a .json file", file=sys.stderr)
        sys.exit(1)

    config = GameConfig.load_config(args.config_file)
    engine = Engine(config)
    engine.run()


if __name__ == "__main__":
    main()
