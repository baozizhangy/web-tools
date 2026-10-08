"""
ASGI config for djangoWebTools project.

组合 Django WSGI 和 MCP HTTP/SSE 两个子应用：
  - /mcp/*  → MCP SSE 服务（JSON-RPC 造数工具）
  - 其他     → Django 应用

通过 Uvicorn 启动:
    uvicorn djangoWebTools.asgi:application --host 0.0.0.0 --port 8000
"""
import os

from django.core.asgi import get_asgi_application
from mcp_server.http_app import create_http_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoWebTools.settings')

django_app = get_asgi_application()
mcp_app = create_http_app()


async def application(scope, receive, send):
    """
    组合 ASGI 应用：根据路径前缀分流。

    /mcp 流量 → MCP SSE app（路径重写去掉前缀，匹配 Starlette 路由）
    其他流量 → Django ASGI
    """
    if scope['type'] == 'lifespan':
        await mcp_app(scope, receive, send)
    elif scope['path'].startswith('/mcp'):
        # 去掉 /mcp 前缀，使 /mcp/sse → /sse、/mcp/messages → /messages
        # 匹配 Starlette SSE app 内部路由
        new_scope = dict(scope)
        new_scope['path'] = scope['path'][4:] or '/'
        await mcp_app(new_scope, receive, send)
    else:
        await django_app(scope, receive, send)
