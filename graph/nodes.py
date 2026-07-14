# ============================================================
# 文件：graph/nodes.py
# 作用：实现三个核心节点函数
# ============================================================


from graph.state import OrderState  # 导入状态数据结构 OrderState
from graph.llm_client import get_deepseek_llm   # 导入工厂函数 get_deepseek_llm，用于创建配置好的 DeepSeek LLM 实例
from tools.supplier_risk_check import check_supplier_risk   # 导入工具函数 check_supplier_risk，用于查询供应商风险数据
from utils.order_loader import load_order   # Day5新增，导入统一加载接口


# 第1个节点：解析订单
def parser_order(state: OrderState):
    """
    解析订单信息，提取关键信息并更新状态
    目前使用模拟数据（硬编码），后续改为从excel和pdf读取
    """

    # 模拟从订单文件解析出的数据
    # 实际场景中，这里会调用 utils/excel_parser.py 或 utils/pdf_parser.py
    return {
        "supplier_name": "噜噜王国",    # 供应商名称
        "total_mount": 125000.0,          # 订单总金额
        "delivery_date": "2026-08-15",    # 交货日期
        "contract_clauses": [
            "合同条款1：供应商需按时交货，否则需支付违约金。",
            "合同条款2：供应商需提供质量保证，若产品不符合标准，需退货并赔偿损失。",
            "合同条款3：付款方式为货到付款，供应商需提供合法发票。"
        ],
        "order_id": "PO-2026-002"  # 订单ID
    }

# 第2个节点：风险分析 Day5更新，替换之前的固定数据，改为从文件加载订单数据
def risk_analysis(state: OrderState) -> dict:
    """
    从文件加载订单数据（替换之前的硬编码数据）。
    """

    # 第1步：从state中获取文件路径
    file_path = state.get("file_path", "mock_order.xlsx")

    # 第2步：尝试加载文件
    try:
        order_data = load_order(file_path)
        print(f"√ 成功加载订单文件：{file_path}")
        return order_data
    except FileNotFoundError:
        # 文件不存在时兜底方案
        print(f"！文件不存在：{file_path},使用默认模拟数据")
        return{
            "order_id": "PO-DEFAULT",
            "supplier_name": "噜噜王国",
            "total_amount": 100000.0,
            "delivery_date": "2026-08-01",
            "contract_clause": "逾期交货违约金：每延迟一日，支付合同总金额的0.05%"
        }
    
    except Exception as e:
        # 其他解析错误（如格式不匹配）的兜底方案
        print(f"×解析失败：{file_path},使用默认模拟数据")
        return{
            "order_id": "PO-ERROR",
            "supplier_name": "噜噜王国",
            "total_amount": 100000.0,
            "delivery_date": "2026-08-01",
            "contract_clause": "逾期交货违约金：每延迟一日，支付合同总金额的0.05%"
        }


# # 第2个节点：风险分析
# def risk_analysis(state: OrderState) ->dict:
#     """
#     调用DS分析合同条款的风险，并更新状态中的风险评分、风险等级和风险点列表
#     """

#     # 获取LLM实例，使用指定推理强度
#     llm = get_deepseek_llm(temperature=0.3, reasoning_effort="medium")

#     # 构造提示词
#     prompt = f"""
#     你是一个采购订单审核专家，请根据以下合同条款分析：

#     合同条款如下：
#     {state.get("contract_clauses")}

#     请输出：
#     1.风险等级（低、中、高）
#     2.风险点列表（用分号分隔）
#     3.风险评分（0~100，越高风险越大）
#     4.简要理由
#     """

#     # 调用LLM（同步阻塞，返回一个响应对象
#     response = llm.invoke([{"role": "user", "content": prompt}])
#     content = response.content

#     # 解析LLM的输出，提取风险等级、风险点列表和风险评分
#     risk_level = "中"  # 默认风险等级
#     if "风险等级：高" in content:
#         risk_level = "高"
#     elif "风险等级：低" in content:
#         risk_level = "低"

#     risk_score = 50.00  # 默认风险评分
#     if "风险评分：" in content:
#         try:
#             # 提取“风险评分：”后面的数字部分
#             score_str = content.split("风险评分：")[1].split()[0]
#             risk_score = float(score_str)
#         except:
#             # 如果解析失败，根据风险等级赋一个合理值
#             if risk_level == "高":
#                 risk_score = 80.00
#             elif risk_level == "中":
#                 risk_score = 50.00
#             else:
#                 risk_score = 20.00
#     else:
#         # 如果LLM没输出"风险评分："，根据风险等级自动赋值
#         if risk_level == "高":
#             risk_score = 80.00
#         elif risk_level == "中":
#             risk_score = 50.00
#         else:
#             risk_score = 20.00
    
#     risk_points = []
#     if "风险点：" in content:
#         try:
#             # 提取 "风险点：" 后面到下一个关键词（或行尾）的内容
#             points_part = content.split("风险点：")[1].split("简要理由")[0]
#             risk_points = [p.strip() for p in points_part.split("；") if p.strip()]
#         except IndexError:
#             # 如果解析失败，保持空列表
#             pass

#     # 返回需更新的字段
#     return {
#         "risk_level": risk_level,   # 保存风险等级
#         "risk_points": risk_points,  # 保存风险点列表
#         "risk_score":  risk_score, # 保存风险评分
#         "risk_analysis_full": content  # 保存完整的LLM分析结果，便于后续调试和审计
#     }

# 第3个节点：供应商核验
def supplier_verify(state: OrderState) -> dict:
    """
    调用工具函数 check_supplier_risk 查询供应商风险数据，并更新状态中的供应商核验结果
    """

    # 从state中取出供应商名称，若不存在则用默认值
    supplier_name = state.get("supplier_name", "未知供应商")

    # 调用工具函数返回字典
    result = check_supplier_risk(supplier_name)

    # 返回更新
    return {
        "supplier_risk_data": result,  # 保存供应商核验结果
        "risk_level": result.get("risk_level") #同步到顶层
    }