import argparse
from btweak.helpers.fixthings import fix_berserkarch_gpg_pacman, fix_db_lck
from btweak.helpers.toolhandler import (
    print_groups,
    print_specific_group_by_index,
    install_group,
)  # noqa
from btweak.helpers.fileparser import ToolGroupParser, ContainersGroupParser
from btweak.helpers.dockerhandler import (
    print_all_container_groups,
    print_container_group_by_index,
    print_search_results,
    run_container,
)


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

    # tools group
    tools_subcmd = subcmd.add_parser("tools", help="List, install and remove tools")
    tools_subcmd.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all tools categories and profiles",
    )
    tools_subcmd.add_argument(
        "-g", "--group", type=int, help="List info about a specific group"
    )
    tools_subcmd.add_argument(
        "-i", "--install", type=int, help="Install a specific group"
    )

    # docker containers for systems and tools
    docker_subcmd = subcmd.add_parser(
        "docker", help="List and manage docker images for systems and tools"
    )
    docker_subcmd.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all available options",
    )
    docker_subcmd.add_argument(
        "-g", "--group", type=int, help="List info about a specific group"
    )
    docker_subcmd.add_argument(
        "-s", "--search", type=str, help="Search for available containers"
    )
    docker_subcmd.add_argument(
        "-r", "--run", type=str, help="Run any available containers"
    )

    # parser.add_argument("-v", "--version", action="store_true", help="Get Version Info") # noqa
    return parser, parser.parse_args()


def main():
    FILENAME = "/home/musashi/projects/btweak/btweak/data/tools.yaml"
    DFILENAME = "/home/musashi/projects/btweak/btweak/data/docker.yaml"
    parser, args = parse_args()

    match args.command:
        case "fix":
            if args.gpg:
                fix_berserkarch_gpg_pacman()
            elif args.db_lck:
                fix_db_lck()
            else:
                parser.parse_args(["fix", "--help"])
        case "tools":
            toolsp = ToolGroupParser(FILENAME)
            groups = toolsp.parse()
            if args.list:
                print_groups(groups)
            elif args.group:
                print_specific_group_by_index(args.group, toolsp)
            elif args.install:
                install_group(args.install, toolsp)
            else:
                parser.parse_args(["tools", "--help"])

        case "docker":
            dockerp = ContainersGroupParser(DFILENAME)
            dockerp.parse()
            if args.list:
                print_all_container_groups(dockerp)
            elif args.group:
                print_container_group_by_index(dockerp, args.group)
            elif args.search:
                print_search_results(dockerp, args.search)
            elif args.run:
                run_container(dockerp, args.run)
            else:
                parser.parse_args(["docker", "--help"])
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
