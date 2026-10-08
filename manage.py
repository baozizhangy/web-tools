#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoWebTools.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # # 设置默认的 runserver 主机和端口
    # if 'runserver' in sys.argv:
    #     sys.argv[sys.argv.index('runserver')+1:] = ['0.0.0.0:80']
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    #  启动django项目：python manage.py runserver
    # 局域网可访问：python manage.py runserver 0.0.0.0:8000
    # linux 启动项目：gunicorn djangoWebTools.wsgi 或 gunicorn --bind 0.0.0.0:8080 djangoWebTools.wsgi
    # 指定IP：python manage.py runserver 172.31.255.50:8000
    # 生成依赖：pipreqs . --encoding=utf8 --force --use-local

