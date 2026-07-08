import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import time
from dotenv import load_dotenv
from openai import OpenAI
from tools.supplier_risk_check import check_supplier_risk

load_dotenv()

# ---------- 工具定义（两个模型共用） ----------
tools = [
    {
        "type": "function",          # 固定写法，函数工具
        "function": {
            "name": "check_supplier_risk",           # 函数名称（必须和实际函数保持一致）
            "description": "查询供应商的履约风险，包括历史交货延迟率、质量合格率、资质到期日",  # 功能用途
            "parameters": {          # 定义调用函数所需参数
                "type": "object",    # 参数是一个对象（JSON 格式）
                "properties": {      # 具体的参数列表
                    "supplier_name": {
                        "type": "string",          # 参数类型是字符串
                        "description": "供应商全称，如'华诚供应链'"  # 模型填入参数示例
                    }
                },
                "required": ["supplier_name"]      # 必须提供的参数
            }
        }
    }
]

messages = [
    {"role": "system", "content": "你是采购审核助手，查询供应商风险时必须调用 check_supplier_risk 工具。"},
    {"role": "user", "content": "请帮我查一下供应商'鑫达物流'的风险情况，并给出审核建议。"}
]

# ---------- 测试函数 ----------
def test_model(client, model_name, model_id, thinking_enabled=True):
    """
    执行一次 Function Calling 测试，并返回统计信息
    :param client: OpenAI 客户端
    :param model_name: 显示名称（如 'DeepSeek V4 Flash'）
    :param model_id: API 模型ID（如 'deepseek-v4-flash'）
    :param thinking_enabled: 是否开启深度思考
    """
    print(f"\n{'='*60}")
    print(f" 测试模型: {model_name} (模型ID: {model_id})")
    print(f"{'='*60}")

    # 准备请求参数（根据模型调整）
    params = {
        "model": model_id,
        "messages": messages.copy(),
        "tools": tools,
        "tool_choice": "auto",
        "temperature": 0.3,
        "stream": False,
    }
    # DeepSeek 支持 thinking 和 reasoning_effort
    if "deepseek" in model_id:
        params["extra_body"] = {
        "thinking": {"type": "enabled"} if thinking_enabled else {"type": "disabled"},
        "reasoning_effort": "high" # 按需改成high
    }
    # 智谱 GLM 也可以加思考参数（如果支持），暂不添加，保持兼容

    # ---------- 第一次调用（判断是否需要调用工具） ----------
    start_time = time.time()
    try:
        response = client.chat.completions.create(**params)
        elapsed = time.time() - start_time
    except Exception as e:
        print(f" 请求失败: {e}")
        return None

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # 统计第一次调用的 token 使用
    usage1 = response.usage
    print(f"第一次调用耗时: {elapsed:.2f} 秒")
    print(f"输入 Token: {usage1.prompt_tokens}, 输出 Token: {usage1.completion_tokens}, 总计: {usage1.total_tokens}")

    if not tool_calls:
        print("模型直接回复（未调用工具）:")
        print(response_message.content)
        return {
            "model": model_name,
            "first_call_time": elapsed,
            "total_tokens": usage1.total_tokens,
            "tool_called": False
        }

    # ---------- 执行工具调用 ----------
    print("模型要求调用工具，参数如下：")
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        print(f" 调用函数: {function_name}, 参数: {function_args}")

        if function_name == "check_supplier_risk":
            supplier = function_args.get("supplier_name")
            result = check_supplier_risk(supplier)
            print(f"查询结果: {result}")

            # 把工具结果回传给模型，生成最终回复
            messages_with_tool = messages.copy()
            messages_with_tool.append(response_message)
            messages_with_tool.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })
            print(response.usage)

            # ---------- 第二次调用（生成最终建议） ----------
            params2 = {
                "model": model_id,
                "messages": messages_with_tool,
                "temperature": 0.3,
                "stream": False,
            }
            if "deepseek" in model_id:
                params["extra_body"] = {
                    "thinking": {"type": "enabled"} if thinking_enabled else {"type": "disabled"},"reasoning_effort": "high" # 按需改成high
            }
            start_time2 = time.time()
            try:
                response2 = client.chat.completions.create(**params2)
                elapsed2 = time.time() - start_time2
            except Exception as e:
                print(f"第二次请求失败: {e}")
                return None

            usage2 = response2.usage
            print(f"第二次调用耗时: {elapsed2:.2f} 秒")
            print(f"输入 Token: {usage2.prompt_tokens}, 输出 Token: {usage2.completion_tokens}, 总计: {usage2.total_tokens}")
            print("\n最终审核建议：")
            print(response2.choices[0].message.content)

            # 返回完整统计
            return {
                "model": model_name,
                "first_call_time": elapsed,
                "second_call_time": elapsed2,
                "total_time": elapsed + elapsed2,
                "total_tokens": usage1.total_tokens + usage2.total_tokens,
                "tool_called": True
            }

# ---------- 主程序 ----------
if __name__ == "__main__":
    results = []

    # 1. DeepSeek V4 Flash
    client_ds = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    results.append(test_model(client_ds, "DeepSeek V4 Flash", "deepseek-v4-flash"))

    # 2. 智谱 GLM-5.2
    client_glm = OpenAI(
        api_key=os.getenv("GLM_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
    results.append(test_model(client_glm, "智谱 GLM-5.2", "glm-5.2"))

    # ---------- 打印汇总对比 ----------
    print("\n" + "="*60)
    print("性能对比汇总")
    print("="*60)
    for r in results:
        if r is None:
            continue
        print(f"\n  {r['model']}")
        print(f"   首次调用耗时: {r['first_call_time']:.2f}s")
        if r.get('second_call_time'):
            print(f"   第二次调用耗时: {r['second_call_time']:.2f}s")
            print(f"   总耗时: {r['total_time']:.2f}s")
            print(f"   总计消耗 Token: {r['total_tokens']}")
        else:
            print(f"   总耗时: {r['first_call_time']:.2f}s")
            print(f"   总计消耗 Token: {r['total_tokens']}")
        print(f"   是否调用工具: {'是' if r['tool_called'] else '否'}")