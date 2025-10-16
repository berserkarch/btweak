import subprocess
from typing import Union, List, Dict
from rich import print


def run_system_commands(
    commands: Union[str, List[str]],
    shell: bool = True,
    text: bool = True,
    check: bool = False,
) -> Union[Dict, List[Dict]]:

    def execute_single_command(cmd: str) -> Dict:
        cmd_args = cmd if shell else cmd.split()

        print("[b]>>> {}[/]".format(cmd))
        process = subprocess.Popen(
            cmd_args if isinstance(cmd_args, str) else cmd_args,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=text,
            bufsize=1,
        )

        output = []
        for line in process.stdout:
            print(line, end="")
            output.append(line)

        process.wait()

        # return {"returncode": process.returncode, "output": "".join(output)}

    if isinstance(commands, str):
        # return execute_single_command(commands)
        execute_single_command(commands)
    elif isinstance(commands, list):
        # return [execute_single_command(cmd) for cmd in commands]
        [execute_single_command(cmd) for cmd in commands]
    else:
        raise TypeError("commands must be a string or list of strings")
