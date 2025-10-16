import subprocess
from typing import Union, List, Dict


def run_system_commands(
    commands: Union[str, List[str]],
    shell: bool = True,
    capture_output: bool = True,
    text: bool = True,
    check: bool = False,
) -> Union[Dict, List[Dict]]:

    def execute_single_command(cmd: str) -> Dict:
        try:
            cmd_args = cmd if shell else cmd.split()

            result = subprocess.run(
                cmd_args,
                shell=shell,
                capture_output=capture_output,
                text=text,
                check=check,
            )

            return {
                "command": cmd,
                "returncode": result.returncode,
                "stdout": result.stdout if capture_output else None,
                "stderr": result.stderr if capture_output else None,
                "success": result.returncode == 0,
            }

        except subprocess.CalledProcessError as e:
            return {
                "command": cmd,
                "returncode": e.returncode,
                "stdout": e.stdout if capture_output else None,
                "stderr": e.stderr if capture_output else None,
                "success": False,
                "error": str(e),
            }
        except Exception as e:
            return {
                "command": cmd,
                "returncode": -1,
                "stdout": None,
                "stderr": None,
                "success": False,
                "error": str(e),
            }

    if isinstance(commands, str):
        return execute_single_command(commands)

    elif isinstance(commands, list):
        results = []
        for cmd in commands:
            if isinstance(cmd, str):
                results.append(execute_single_command(cmd))
            else:
                results.append(
                    {
                        "command": str(cmd),
                        "returncode": -1,
                        "stdout": None,
                        "stderr": None,
                        "success": False,
                        "error": "Invalid command type",
                    }
                )
        return results

    else:
        raise TypeError("commands must be a string or list of strings")
