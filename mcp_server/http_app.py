"""
MCP HTTP/SSE ASGI 应用

为嵌入 Django ASGI 服务提供入口。返回 Starlette ASGI 子应用，
挂载路径 /mcp，客户端通过 http://<host>:<port>/mcp/sse 连接。
"""
from mcp_server.server import create_mcp


def create_http_app():
    """
    创建 MCP SSE ASGI 子应用。

    mount_path='/mcp' 确保 SSE transport 返回给客户端的
    message endpoint 为 /mcp/messages/（含前缀，客户端能直接调用）。
    """
    mcp = create_mcp()
    return mcp.sse_app(mount_path="/mcp")
