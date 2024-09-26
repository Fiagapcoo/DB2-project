#!/usr/bin/env python
import os
import sys
from decouple import config

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Get the PORT value from the .env file
    port = config('PORT', default='8000')
    
    # Modify sys.argv if the "runserver" command is being used and no port is provided
    if 'runserver' in sys.argv and len(sys.argv) == 2:
        sys.argv.append(f'0.0.0.0:{port}')
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
