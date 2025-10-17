import yaml
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class Package:
    name: str
    description: str


@dataclass
class ToolGroup:
    name: str
    description: str
    packages: List[Package] = field(default_factory=list)


class ToolGroupParser:
    def __init__(self, yaml_file: str):
        self.yaml_file = yaml_file
        self.tool_groups: List[ToolGroup] = []

    def parse(self) -> List[ToolGroup]:
        with open(self.yaml_file, "r") as f:
            data = yaml.safe_load(f)

        for group_data in data:
            packages = []
            for pkg_data in group_data.get("packages", []):
                pkg = Package(
                    name=pkg_data["name"],
                    description=pkg_data["description"],
                )
                packages.append(pkg)

            tool_group = ToolGroup(
                name=group_data["name"],
                description=group_data["description"],
                packages=packages,
            )
            self.tool_groups.append(tool_group)

        return self.tool_groups

    def get_packages_by_index(self, index: int) -> Optional[List[Package]]:
        try:
            return self.tool_groups[index - 1].packages
        except IndexError:
            return None

    def get_group_by_index(self, index: int) -> Optional[ToolGroup]:
        try:
            return self.tool_groups[index - 1]
        except IndexError:
            return None

    def search_package(self, search_term: str) -> List[tuple]:
        results = []
        for group in self.tool_groups:
            for pkg in group.packages:
                if search_term.lower() in pkg.name.lower():
                    results.append((group.name, pkg))
        return results

    def get_all_packages(self) -> Dict[str, List[Package]]:
        return {group.name: group.packages for group in self.tool_groups}
