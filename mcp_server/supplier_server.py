# ============================================================
# 文件：mcp_server/supplier_server.py
# 作用：将 check_supplier_risk 包装为 MCP Tool
# 适配：mcp==2.0.0b1（使用 add_request_handler 非装饰器模式）
# ============================================================

import sys
import os
import json
import asyncio

# ---- 第1步：添加项目根目录到 Python 路径（用于导入 tools） ----
# 原因：mcp_server 在项目根目录下，导入 tools 需要找到上级目录
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from tools.supplier_risk_check import check_supplier_risk

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio


# ---- 第2步：创建 Server 实例 ----
server = Server("supplier-risk-server")


# ---- 第3步：定义 tools/list 的处理器函数 ----
# 注意：这里不是装饰器，而是一个普通的异步函数
async def handle_tools_list(request):
    """
    处理 tools/list 请求：返回可用的工具列表
    """
    return {
        "tools": [
            {
                "name": "check_supplier_risk",
                "description": "查询供应商的履约风险，包括历史交货延迟率、质量合格率、资质到期日",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "supplier_name": {
                            "type": "string",
                            "description": "供应商全称，如'华诚供应链'",
                        },
                    },
                    "required": ["supplier_name"],
                },
            }
        ]
    }


# ---- 第4步：定义 tools/call 的处理器函数 ----
async def handle_tools_call(request):
    """
    处理 tools/call 请求：执行 check_supplier_risk 并返回结果
    """
    params = request.get("params", {})
    name = params.get("name")
    arguments = params.get("arguments", {})

    if name == "check_supplier_risk":
        supplier_name = arguments.get("supplier_name", "")
        if not supplier_name:
            return {
                "content": [{"type": "text", "text": "错误：缺少 supplier_name 参数"}],
                "isError": True
            }
        result = check_supplier_risk(supplier_name)
        return {
            "content": [
                {"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}
            ]
        }
    else:
        return {
            "content": [{"type": "text", "text": f"错误：未知工具 '{name}'"}],
            "isError": True
        }


# ---- 第5步：注册处理器（非装饰器方式） ----
# add_request_handler 签名：add_request_handler(method, params_type, handler)
# 这里 params_type 传 None 表示不进行参数校验（简化）
server.add_request_handler("tools/list", None, handle_tools_list)
server.add_request_handler("tools/call", None, handle_tools_call)


# ---- 第6步：启动服务器 ----
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="supplier-risk-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())