# 调用API过程记录

1. 虚拟环境激活失败，主要原因在于Python版本没添加环境变量。而使用where python 和Python --version时经常不返回信息，判断是版本太多问题。后面查询到3.9版本可用，将3.9的Path添加到位后，激活成功。

2. 安装python库的时候提示pip版本低，用了命令更新：python -m pip install --upgrade pip

3. 最终以3.9和ds-v4-flash+thinking参数调用DS api成功，GLM的更顺利，没啥问题，直接跑通了。

4. API Key的name由专家模式切换至便宜的v4-flash，主要是专家模式0724下线。

5. DS的响应速度更快。

6. DS的首次调用最好直接用API文档写的，不然可能跑不通。

   ```python
   # DS对话提供的代码
   response_ds = client_ds.chat.completions.create(
       model="deepseek-v4-flash",  # 1. 更新了模型名
       messages=[
           {"role": "system", "content": "你是一位资深的采购合同风险管理专家。"},
           {"role": "user", "content": "请评估一份采购合同中'逾期交货违约金'条款的风险，给出3条修改建议。"}
       temperature=0.3,
       thinking={       # 2. 新增 thinking 参数，显式开启深度思考
           "type": "enabled"
       },
       reasoning_effort="max"  # 可选，设置思考强度
   )
   # 这个报错：❌ DeepSeek 报错: create() got an unexpected keyword argument 'thinking'   参数有问题！！！
   
   # 后来参考DS官方文档，参数问题解决
       response_ds = client_ds.chat.completions.create(
           model="deepseek-v4-flash",
           messages=[
               {"role": "system", "content": "你是一位资深的采购合同风险管理专家。"},
               {"role": "user", "content": "请评估一份采购合同中'逾期交货违约金'条款的风险，给出3条修改建议。"}
           ],
           temperature=0.3,
           stream=False,
           reasoning_effort="high",
           extra_body={"thinking": {"type": "enabled"}}
       )
       print(response_ds.choices[0].message.content)
   ```

7. 需要注意的是DS的reasoning_effort真正用的时候要改成high，medium有点降智。

8. 加了一个运行时间统计。

   - 其实优先级应该是跑通＞性能统计。
   - 最初运行时一直提示没有tools的库，此时应该敏感点的，作为函数应该需要提前定义，不能在一个脚本中调用不存在的自己。
   - DS给的建议也有误导，应该提示他在没有定义函数前不能直接调用功能。
   - 在理清楚先有鸡还是先有蛋以后，先梳理了整体的项目结构，把scripts\tools\docs等并列处理。tools里面提前定义好function，然后在second_call.py(需要执行的脚本)内声明和调用。

9. 在实际运行过程中，发现DS老是调用不成功，后面发现报错总是卡在params的thinking处，琢磨后估计是写法不对，截图给DS才研究出来：

   - **openai 库的 create() 方法只接受官方定义的参数（如 model、messages、temperature 等）。**
   - **各厂商（如 DeepSeek、智谱）提供的扩展功能（如深度思考、推理强度）不属于 OpenAI 官方参数，必须通过 extra_body 作为“容器”传递，库会将 extra_body 的内容原样合并到 HTTP 请求体中。**

10. 更改写法后运行成功。

11. 然后发现GLM调用不成功，原因是我在统计token时加入了ds有的是否命中缓存token统计，而GLM并没有这个object，因此一直报错。

12. 后面为了兼容这两个模型，把是否命中缓存token的信息删掉，运行均跑通了。

# 最终输入

```python
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
```



# 最终输出

> ============================================================
>
>  测试模型: DeepSeek V4 Flash (模型ID: deepseek-v4-flash)
> ============================================================
>
> 第一次调用耗时: 6.33 秒
> 输入 Token: 344, 输出 Token: 80, 总计: 424
> 模型要求调用工具，参数如下：
>  调用函数: check_supplier_risk, 参数: {'supplier_name': '鑫达物流'}
> 查询结果: {'supplier_name': '鑫达物流', 'delay_rate': 0.23, 'quality_pass_rate': 0.87, 'cert_expire': '2026-09-15', 'risk_level': '高风险', 'recommendation': '建议暂停合作，启动备选供应商排查', 'data_source': 'Mock DB (模拟数据，非真实查询)'}
> CompletionUsage(completion_tokens=80, prompt_tokens=344, total_tokens=424, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=16, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=256), prompt_cache_hit_tokens=256, prompt_cache_miss_tokens=88)
> 第二次调用耗时: 6.30 秒
> 输入 Token: 213, 输出 Token: 498, 总计: 711
>
> 最终审核建议：
>
> ## 供应商“鑫达物流”风险审查报告
>
> ### 📊 风险指标概览
>
> | 评估项         | 数据         | 判断                   |
> | -------------- | ------------ | ---------------------- |
> | **风险等级**   | 🔴 **高风险** | 需要密切关注           |
> | **交付延迟率** | 23%          | 偏高（行业通常＜10%）  |
> | **质量合格率** | 87%          | 低于优质线（通常≥95%） |
> | **资质有效期** | 2026-09-15   | 目前有效，但接近中期   |
>
> ### ⚠️ 主要风险点
>
> 1. **交付稳定性差**：延迟率接近四分之一，可能影响您的供应链节奏和客户交付承诺。
> 2. **质量合格率偏低**：87%意味着每100单中约有13单存在质量问题，退货/返工成本较高。
> 3. **综合高风险评级**：系统建议暂停合作。
>
> ### ✅ 审核建议
>
> | 优先度 | 行动项                 | 说明                                                        |
> | ------ | ---------------------- | ----------------------------------------------------------- |
> | 🔴 紧急 | **启动备选供应商排查** | 尽快寻找替代物流供应商，降低单一依赖风险                    |
> | 🟡 中   | **与鑫达物流约谈**     | 要求其提交改进计划，特别是延迟和质量改善措施                |
> | 🟢 常规 | **设定观察期**         | 如无法立即切换，可设置1~2个月观察期，达标率未改善则终止合作 |
> | 📋 文档 | **记录本次评估**       | 存档备查，作为供应商绩效评价的补充材料                      |
>
> ### 📝 总结建议
>
> **最优选择**：建议 **暂停新订单下发**，优先启动备选供应商的评估和试单流程。  
> **过渡方案**：若业务无法立即切换，可要求鑫达物流缴纳**履约保证金**或提供**延迟赔付承诺**，并设置质量合格率≥90%的底线。
>
> > ⚡ 注：以上数据来源于Mock DB模拟查询，仅供演示参考。实际审核时请结合真实系统数据进行决策。
>
> ============================================================
>
>  测试模型: 智谱 GLM-5.2 (模型ID: glm-5.2)
> ============================================================
>
> 第一次调用耗时: 6.13 秒
> 输入 Token: 227, 输出 Token: 69, 总计: 296
> 模型要求调用工具，参数如下：
>  调用函数: check_supplier_risk, 参数: {'supplier_name': '鑫达物流'}
> 查询结果: {'supplier_name': '鑫达物流', 'delay_rate': 0.23, 'quality_pass_rate': 0.87, 'cert_expire': '2026-09-15', 'risk_level': '高风险', 'recommendation': '建议暂停合作，启动备选供应商排查', 'data_source': 'Mock DB (模拟数据，非真实查询)'}
> CompletionUsage(completion_tokens=69, prompt_tokens=227, total_tokens=296, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=33, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0))
> 第二次调用耗时: 18.16 秒
> 输入 Token: 201, 输出 Token: 573, 总计: 774
>
> 最终审核建议：
>
> ## 供应商风险查询结果 — 鑫达物流
>
> 以下是该供应商的风险详情：
>
> | 风险维度         | 评估结果     | 风险说明                                                     |
> | ---------------- | ------------ | ------------------------------------------------------------ |
> | **交付延迟率**   | 23%          | 延迟率偏高，超过五分之一的订单存在交付延迟，严重影响供应链稳定性 |
> | **质量合格率**   | 87%          | 低于行业优质供应商水平（通常≥95%），存在质量管控隐患         |
> | **资质有效期**   | 2026-09-15   | 资质证书目前仍在有效期内，暂无过期风险                       |
> | **综合风险等级** | 🔴 **高风险** | 多项指标不达标，综合评估为高风险供应商                       |
>
> ---
>
> ## 📋 审核建议
>
> ### 1. 短期措施（立即执行）
>
> - **暂停新增合作订单**：鉴于延迟率高达23%且质量合格率仅87%，建议暂停向该供应商下达新采购订单。
> - **启动备选供应商排查**：立即开展物流备选供应商的资质审核与询价工作，确保供应链不中断。
>
> ### 2. 中期措施（1-3个月内）
>
> - **约谈供应商管理层**：要求鑫达物流就交付延迟和质量问题提交书面整改方案，明确改善时间表和量化目标。
> - **加强到货检验**：在过渡期内，对该供应商的每一批次货物进行严格的质量检验，增加抽检比例。
> - **设置改善考核期**：给予1-3个月的观察期，要求延迟率降至10%以下、质量合格率提升至95%以上。
>
> ### 3. 长期措施
>
> - **建立供应商动态评估机制**：定期（如每季度）对所有供应商进行风险评级，实现优胜劣汰。
> - **完善合同条款**：在采购合同中增加延迟交付和质量不合格的违约赔偿条款，降低采购风险。
>
> ---
>
> > ⚠️ **提示**：以上数据来源于模拟数据库，实际审核请以真实业务数据为准。如需进一步调查或有其他供应商需要评估，请随时告知。
>
> ============================================================
>
> 性能对比汇总
> ============================================================
>
>   DeepSeek V4 Flash
>    首次调用耗时: 6.33s
>    第二次调用耗时: 6.30s
>    总耗时: 12.63s
>    总计消耗 Token: 1135
>    是否调用工具: 是
>
>   智谱 GLM-5.2
>    首次调用耗时: 6.13s
>    第二次调用耗时: 18.16s
>    总耗时: 24.29s
>    总计消耗 Token: 1070
>    是否调用工具: 是
