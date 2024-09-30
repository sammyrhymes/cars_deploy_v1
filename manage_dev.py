"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import Config, RepositoryEnv

# Load .env.dev for development
current_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path to the directory of this script
env_file_path = os.path.join(current_dir, '.env.dev')  # Path to the .env.dev file in the same directory as manage_dev.py

# Verify if the file exists
if not os.path.exists(env_file_path):
    raise FileNotFoundError(f"{env_file_path} not found.")

config = Config(RepositoryEnv(env_file_path))


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_competition.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
