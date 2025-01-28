
import argparse
import os
import subprocess
import sys
from typing import Iterable

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"


def run_command_with_output(command) -> tuple[str, bool]:
    command_text = " ".join(command)
    print(f"-> {GREEN}{command_text}{RESET}")

    # Running the command
    success = True
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        success = False
        output = e.output

    print(f"{BLUE}{output}{RESET}")

    return output, success


def exec_command(command) -> bool:
    command_text = " ".join(command)
    print(f"-> {GREEN}{command_text}{RESET}")

    # Running the command
    success = True
    try:
        output = subprocess.run(command)
    except subprocess.CalledProcessError:
        success = False
        output = None

    if success and output is not None and output.returncode != 0:
        success = False

    return success


def check_if_container_running(container_name):
    # check if container exists and is running:
    running_container_id = run_command_with_output(
        ["docker", "ps", "-q", "-f", f"name={container_name}", "-f", "status=running"]
    )[0].strip()
    return running_container_id != ""


def remove_container_if_not_running(container_name) -> bool:
    if check_if_container_running(container_name):
        return False

    container_id = run_command_with_output(
        ["docker", "ps", "-a", "-q", "-f", f"name={container_name}"]
    )[0].strip()
    if container_id != "":
        run_command_with_output(["docker", "rm", container_id])
        return True
    return False


def get_git_repo_names() -> list[str]:
    return [
        "spinningup",
    ]


def get_path_mounts() -> list[tuple[str, str]]:
    home_full_path = os.path.expanduser("~")
    workdir = f"{home_full_path}/spinningup/workdir"

    repo_names = get_git_repo_names()
    return [
        # utils
        (f"{workdir}/.zsh_history", "/root/.zsh_history"),
        (f"{workdir}/.zshrc", "/root/.zshrc"),
        (f"{workdir}/.p10k.zsh", "/root/.p10k.zsh"),
    ] + [
        # repo
        (f"{home_full_path}/{repo_name}", f"/root/{repo_name}")
        for repo_name in repo_names
    ]


def make_mount_args() -> Iterable[str]:
    for src, target in get_path_mounts():
        if not os.path.exists(src):
            print(f"{RED}Directory {src} does not exist. Skipping mount.{RESET}")
            continue

        arg = f"--mount=type=bind,source={src},target={target}"
        yield arg


def system_wide_opts_for_docker_run() -> Iterable[str]:
    options = [
        "--gpus=all",
        "--net=host",  # Required for passing through host ports.
        "--privileged",  # Required for passing through USB devices.
        "--runtime=nvidia",
    ]
    return options


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Run the shapgs docker container")
    parser.add_argument(
        "--image-name", type=str, default="v0", help="Name of the docker image"
    )
    parser.add_argument(
        "--suffix", type=str, default="", help="Suffix to add to the container name"
    )
    args = parser.parse_args()
    if args.suffix:
        container_name = f"{os.getenv('USER')}-{args.image_name.split('/')[-1]}-{args.suffix}"
    else:
        container_name = f"{os.getenv('USER')}-{args.image_name.split('/')[-1]}"
    if check_if_container_running(container_name):
        # If container exists, use docker exec
        exec_command(
            [
                "docker",
                "exec",
                *(["-it"] if sys.stdin.isatty() else []),
                container_name,
                "zsh",
            ]
        )
    else:
        remove_container_if_not_running(container_name)
        # If container does not exist, use docker run
        exec_command(
            [
                "docker",
                "run",
                "--name",
                container_name,
                *(["-it"] if sys.stdin.isatty() else []),
            ]
            + list(system_wide_opts_for_docker_run())
            + list(make_mount_args())
            + ["--shm-size=7G"]
            + [
                args.image_name,
                "zsh",
            ]
        )


if __name__ == "__main__":
    main()
