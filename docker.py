#!/usr/bin/env python3

import argparse
import subprocess

PROJECT_NAME = "alfawal-uav-project"
COMPOSE_FILE = "./docker/docker-compose.yaml"
CONTAINER_NAME = f"{PROJECT_NAME}-django"
CYAN = "\033[96m"
NC = "\033[0m"  # No color (aka. RESET)


def run_command(command: str) -> None:
    """Run a command in the shell.

    Args:
        command (str): Command to run.
    """
    print(f"{CYAN}Running the command:\n{command}{NC}")
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print(f"{CYAN}Interrupted the command:\n{command}{NC}")


def docker_command(*args) -> None:
    """Run a docker command with the specified arguments.

    Args:
        *args: Command line arguments to pass to docker.
    """
    command_parts = (
        "docker",
        "exec",
        "-it",
        CONTAINER_NAME,
        *args,
    )
    full_command = " ".join(command_parts)
    run_command(full_command)


def docker_compose_command(*args) -> None:
    """Run a docker-compose command with the specified arguments.

    Args:
        *args: Command line arguments to pass to docker-compose.
    """
    command_parts = (
        "docker-compose",
        "-f",
        COMPOSE_FILE,
        "-p",
        PROJECT_NAME,
        *args,
    )
    full_command = " ".join(command_parts)
    run_command(full_command)


def manage_py(*args) -> None:
    """Run a Django management command in the Django container.

    Args:
        *args: Command line arguments to pass to manage.py.
    """
    docker_command("python", "manage.py", *args)


def get_parser() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments namespace object.
    """
    parser = argparse.ArgumentParser(
        description="Manage docker-compose and Django management commands."
    )
    parser.add_argument(
        "-c",
        "--command",
        nargs=argparse.REMAINDER,
        help="Command to pass to manage.py",
    )
    subparsers = parser.add_subparsers(dest="compose_command")

    # Docker compose commands
    subparsers.add_parser(
        "build",
        help="Build the docker containers.",
    )

    up_parser = subparsers.add_parser(
        "up",
        help=(
            "Start the docker containers,"
            " -d (--detached) to run in detached mode."
        ),
    )
    up_parser.add_argument(
        "-d",
        "--detached",
        action="store_true",
        help="Run in detached mode.",
    )

    subparsers.add_parser(
        "down",
        help="Stop and remove the docker containers.",
    )
    subparsers.add_parser(
        "stop",
        help="Stop the docker containers.",
    )
    subparsers.add_parser(
        "remove",
        help="Remove the docker containers.",
    )
    subparsers.add_parser(
        "shell",
        help="Open the Django shell in the Django container.",
    )
    subparsers.add_parser(
        "console",
        help="Open a console in the Django container.",
    )
    subparsers.add_parser(
        "makemigrations",
        help="Make migrations.",
    )
    subparsers.add_parser(
        "migrate",
        help="Run migrations.",
    )

    return parser


def main() -> int:
    """Parse arguments and execute the appropriate command."""
    parser = get_parser()
    args = parser.parse_args()
    compose_command = args.compose_command
    if compose_command is None:
        print("No command specified.")
        parser.print_help()
        return 1

    if args.command:
        manage_py(*args.command)
    elif compose_command == "build":
        docker_compose_command("build")
    elif compose_command == "up":
        if args.detached:
            docker_compose_command("up", "-d")
        else:
            docker_compose_command("up")
    elif compose_command == "down":
        docker_compose_command("down")
    elif compose_command == "stop":
        docker_compose_command("stop")
    elif compose_command == "remove":
        docker_compose_command("rm", "-f")
    elif compose_command == "shell":
        manage_py("shell")
    elif compose_command == "console":
        docker_command("sh")
    elif compose_command == "makemigrations":
        manage_py("makemigrations")
    elif compose_command == "migrate":
        manage_py("migrate")
    else:
        print(f"Unknown command: {compose_command}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
