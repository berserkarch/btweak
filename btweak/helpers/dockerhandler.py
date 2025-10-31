from rich.console import Console
from rich.tree import Tree
from btweak.helpers.cmdhandler import run_system_commands

console = Console()


def print_all_container_groups(parser):
    main_tree = Tree("[bold blue]═══ Container Groups ═══[/]")

    for idx, group in enumerate(parser.container_groups, start=1):
        group_branch = main_tree.add(f"[bold cyan]{idx}. {group.name}[/]")
        group_branch.add(f"[dim italic]{group.description}[/]")

        if hasattr(group, "categories") and group.categories:
            total_containers = sum(len(cat.containers) for cat in group.categories)
            group_branch.add(
                f"[yellow]{len(group.categories)} categories, {total_containers} total containers[/]"
            )

            categories_branch = group_branch.add("[bold magenta]Categories:[/]")
            for cat_idx, category in enumerate(group.categories, start=1):
                cat_branch = categories_branch.add(
                    f"[magenta]{cat_idx}. {category.name}[/] [dim]({len(category.containers)} containers)[/]"
                )
                cat_branch.add(f"[dim italic]{category.description}[/]")

                # containers_list = cat_branch.add("[green]Containers:[/]")
                # for container in category.containers:
                #     containers_list.add(f"[green]• {container.name}[/]")

        elif hasattr(group, "containers") and group.containers:
            containers_branch = group_branch.add(
                f"[yellow]{len(group.containers)} containers available[/]"
            )
            for container in group.containers:
                containers_branch.add(f"[green]▸ {container.name}[/]")

    console.print()
    console.print(main_tree)
    console.print()


def print_container_group_by_index(parser, index: int):
    group = parser.get_group_by_index(index)

    if group is None:
        error_tree = Tree("[bold red]✗ Error[/]")
        error_tree.add(f"Invalid index: {index}")
        error_tree.add(f"Available indices: 1-{len(parser.container_groups)}")
        console.print(error_tree)
        return

    main_tree = Tree(f"[bold blue]{group.name}[/]")
    main_tree.add(f"[dim italic]{group.description}[/]")

    if hasattr(group, "categories") and group.categories:
        total_containers = sum(len(cat.containers) for cat in group.categories)
        main_tree.add(
            f"[yellow]Total: {len(group.categories)} categories, {total_containers} containers[/]"
        )

        for cat_idx, category in enumerate(group.categories, start=1):
            category_branch = main_tree.add(
                f"[bold magenta]{cat_idx}. {category.name}[/]"
            )
            category_branch.add(f"[dim italic]{category.description}[/]")

            for idx, container in enumerate(category.containers, start=1):
                container_branch = category_branch.add(
                    f"[bold green]{cat_idx}.{idx}. {container.name}[/]"
                )
                container_branch.add(f"[white]{container.description}[/]")

                commands_branch = container_branch.add("[bold cyan]Commands:[/]")
                commands_branch.add(f"[blue]Pull:[/] {container.command}")
                commands_branch.add(f"[yellow]Run:[/] {container.run}")

    elif hasattr(group, "containers") and group.containers:
        main_tree.add(f"[yellow]Total: {len(group.containers)} containers[/]")

        for idx, container in enumerate(group.containers, start=1):
            container_branch = main_tree.add(f"[bold green]{idx}. {container.name}[/]")
            container_branch.add(f"[white]{container.description}[/]")

            commands_branch = container_branch.add("[bold cyan]Commands:[/]")
            commands_branch.add(f"[blue]Pull:[/] {container.command}")
            commands_branch.add(f"[yellow]Run:[/] {container.run}")

    console.print()
    console.print(main_tree)
    console.print()


def print_search_results(parser, search_term: str):
    console = Console()

    results = parser.search_container(search_term)

    if not results:
        tree = Tree(f"[bold yellow]Search: '{search_term}'[/]")
        tree.add("[dim]No results found[/]")
        console.print(tree)
        return

    tree = Tree(f"[bold cyan]Search Results for '{search_term}'[/]")
    tree.add(f"[yellow]Found {len(results)} container(s)[/]")

    for result in results:
        if len(result) == 3:
            group_name, category_name, container = result
            result_branch = tree.add(f"[green]{container.name}[/]")
            result_branch.add(
                f"[dim]Group: {group_name} → Category: {category_name}[/]"
            )
        else:
            group_name, container = result
            result_branch = tree.add(f"[green]{container.name}[/]")
            result_branch.add(f"[dim]Group: {group_name}[/]")

        result_branch.add(f"[white]{container.description}[/]")

        commands_branch = result_branch.add("[bold cyan]Commands:[/]")
        commands_branch.add(f"[blue]Pull:[/] {container.command}")
        commands_branch.add(f"[yellow]Run:[/] {container.run}")

    console.print()
    console.print(tree)
    console.print()


def run_container(parser, search_term: str):
    console = Console()

    results = parser.search_container(search_term)

    if not results:
        tree = Tree(f"[bold yellow]Search: '{search_term}'[/]")
        tree.add("[dim]No results found[/]")
        console.print(tree)
        return
    elif len(results) == 1:
        container = results[0][-1]
        print(container.run)
        run_system_commands(
            [
                "kitty --hold tmux new-session {}".format(container.run),
            ]
        )
        return
    else:
        tree = Tree(f"[bold cyan]Multiple Results for '{search_term}'[/]")
        tree.add(f"[yellow]Found {len(results)} container(s)[/]")

        for result in results:
            if len(result) == 3:
                group_name, category_name, container = result
                result_branch = tree.add(f"[green]{container.name}[/]")
                result_branch.add(
                    f"[dim]Group: {group_name} → Category: {category_name}[/]"
                )
            else:
                group_name, container = result
                result_branch = tree.add(f"[green]{container.name}[/]")
                result_branch.add(f"[dim]Group: {group_name}[/]")

            result_branch.add(f"[white]{container.description}[/]")

            commands_branch = result_branch.add("[bold cyan]Commands:[/]")
            commands_branch.add(f"[blue]Pull:[/] {container.command}")
            commands_branch.add(f"[yellow]Run:[/] {container.run}")

    console.print()
    console.print(tree)
    console.print()
