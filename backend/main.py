import argparse
from .core.sidekick_core import sidekick_core


def main():
    parser = argparse.ArgumentParser(description="Run Sidekick AI assistant")
    parser.add_argument("--notes", required=True, help="Notes to process")
    args = parser.parse_args()
    sidekick_core(args.notes)


if __name__ == "__main__":
    main()
