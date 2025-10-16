import argparse

# from rich import print


def parse_args():
    p = argparse.ArgumentParser(prog="btweak", description="Berserk Arch Tweak Tool")
    p.add_argument("-v", "--version", action="store_true", help="Get Version Info")

    return p.parse_args()


def main():
    args = parse_args()


if __name__ == "__main__":
    main()
