import os
import sys


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    os.environ['DJANGAE_APP_YAML_LOCATION'] = os.path.abspath(
        os.path.dirname(__file__)
        )
    from djangae.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
