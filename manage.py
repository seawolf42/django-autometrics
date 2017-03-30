import os
import sys


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    sys.path.insert(1, os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'sitepackages',
        ))
    from djangae.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
