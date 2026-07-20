import asyncio
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

server = Server("demo-server")

async def tools_list_handler(request):
    return {
        "tools": [
            {
                "name": "echo",
                "description": "将输入的消息原样返回",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "要回显的消息内容"}
                    },
                    "required": ["message"],
                },
            }
        ]
    }

async def tools_call_handler(request):
    params = request.get("params", {})
    name = params.get("name")
    arguments = params.get("arguments", {})
    if name == "echo":
        message = arguments.get("message", "")
        return {"content": [{"type": "text", "text": f"Echo: {message}"}]}
    return {"content": [{"type": "text", "text": f"错误：未知工具 '{name}'"}], "isError": True}

server.add_request_handler("tools/list", None, tools_list_handler)
server.add_request_handler("tools/call", None, tools_call_handler)

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="demo-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(),  # ← 关键修复
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())