# MCP 配置记录（Cline）

> 日期：2026-07-22  
> 用途：记录 Cline 中 MCP Server 的配置，便于后续复现

## 1. Cline MCP 配置（`cline_mcp_settings.json`）

```json
{
  "mcpServers": {
    "supplier-risk": {
      "command": "D:/工作集合/1zhouxu48/2.9-AI员工专项/2.9.0-【AI先锋】/1-自我提升/ai-pm-learning-journey-main/venv_ai/Scripts/python.exe",
      "args": [
        "-m",
        "mcp_server.supplier_server"
      ],
      "cwd": "D:/工作集合/1zhouxu48/2.9-AI员工专项/2.9.0-【AI先锋】/1-自我提升/ai-pm-learning-journey-main",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  }
}

## 2. 关键说明
command 使用虚拟环境的完整 Python 路径，避免依赖系统 PATH

cwd 为项目根目录的绝对路径

PYTHONPATH 确保 Python 能正确找到 tools/ 和 mcp_server/ 模块

## 3. 验证命令
bash
python -m mcp_server.supplier_server
启动后无任何输出，光标停留，表示服务器正在等待连接。

## 4. 测试结果
供应商	风险等级	状态
华诚供应链	低风险	✅
鑫达物流	高风险	✅