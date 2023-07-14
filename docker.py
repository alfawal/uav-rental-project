#!/usr/bin/env python3

import argparse
import subprocess

PROJECT_NAME = "alfawal-uav-project"
COMPOSE_FILE = "./docker/docker-compose.yaml"
CONTAINER_NAME = "alfawal-uav-project-django"
CYAN = "\033[96m"
NC = "\033[0m"  # No color (aka. RESET)


def docker_compose(*args) -> None:
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
    print(f"{CYAN}Running: {' '.join(command_parts)}{NC}")
    subprocess.run(command_parts)


def manage_py(*args) -> None:
    """Run a Django management command in the Django container.

    Args:
        *args: Command line arguments to pass to manage.py.
    """
    docker_compose("exec", CONTAINER_NAME, "python", "manage.py", *args)


def parse_arguments() -> argparse.Namespace:
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
    up_parser.add_argument(
        "-m",
        "--migrate",
        action="store_true",
        help="Run migrations after starting the containers.",
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
        help="Open a shell in the Django container.",
    )

    return parser.parse_args()


def main() -> None:
    """Parse arguments and execute the appropriate command."""
    args = parse_arguments()

    if args.command:
        manage_py(*args.command)
    elif args.compose_command == "build":
        docker_compose("build")
    elif args.compose_command == "up":
        if args.detached:
            docker_compose("up", "-d")
        else:
            docker_compose("up")

        if args.migrate:
            manage_py("migrate")
    elif args.compose_command == "down":
        docker_compose("down")
    elif args.compose_command == "stop":
        docker_compose("stop")
    elif args.compose_command == "remove":
        docker_compose("rm", "-f")
    elif args.compose_command == "shell":
        docker_compose("exec", CONTAINER_NAME, "bash")
    else:
        print(f"Unknown command: {args.compose_command}")


if __name__ == "__main__":
    raise SystemExit(main())
