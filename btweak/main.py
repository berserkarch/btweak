import argparse
from btweak.helpers.fixthings import fix_berserkarch_gpg_pacman, fix_db_lck


def parse_args():
    parser = argparse.ArgumentParser(
        prog="btweak", description="Berserk Arch Tweak Tool"
    )

    subcmd = parser.add_subparsers(dest="command", required=True)

    # fix things in berserkarch
    fix_subcmd = subcmd.add_parser("fix", help="Fix things in berserkarch")
    fix_subcmd.add_argument(
        "-g", "--gpg", action="store_true", help="Fix pacman gpg key issue"
    )
    fix_subcmd.add_argument(
        "--db-lck",
        action="store_true",
        help="Fix pacman -- unable to lock database error",
    )

    # parser.add_argument("-v", "--version", action="store_true", help="Get Version Info")
    return parser, parser.parse_args()


def main():
    parser, args = parse_args()

    match args.command:
        case "fix":
            if args.gpg:
                fix_berserkarch_gpg_pacman()
            elif args.db_lck:
                fix_db_lck()
            else:
                parser.parse_args(["fix", "--help"])
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
