from pathlib import Path

from dotenv import load_dotenv
from envanter import EnvironmentParser

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Envanter(EnvironmentParser):
    """Environment variables parser."""

    def __init__(self):
        """Loads the environment variables from .env file."""
        super().__init__()
        load_dotenv(dotenv_path=BASE_DIR / ".env")


env = Envanter()
