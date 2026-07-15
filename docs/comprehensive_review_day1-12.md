## comprehensive_review_day1-12

> **复盘周期**：2026-07-06（Day 1）～ 2026-07-15（Day 12）
> **完成阶段**：阶段一（基础搭建）前半程

### 一、总体概况

#### 1.1 背景与目标

| 项目             | 内容                                                         |
| :--------------- | :----------------------------------------------------------- |
| **学习者背景**   | 3年采购/物流/仓储/电商 IT 企业服务经验                       |
| **转型目标**     | AI 产品经理                                                  |
| **核心定位**     | 行业 Know-how + AI 杠杆 = 复合型 AI PM                       |
| **70天计划目标** | 从 0 到 1 搭建采购订单智能审核 Agent，掌握 LangGraph、MCP、多 Agent 协同 |

#### 1.2 核心成果总览

| 维度            | 成果                                                       |
| :-------------- | :--------------------------------------------------------- |
| **GitHub 仓库** | 15+ commits，完整项目结构                                  |
| **模型选型**    | DeepSeek V4 Flash + GLM-5.2 双主力                         |
| **技术栈掌握**  | LangGraph、Function Calling、MCP 协议（入门）、MemorySaver |
| **代码量**      | 10+ Python 文件，约 800+ 行核心代码                        |
| **文档产出**    | 模型对比笔记、周级复盘、状态流转图、README                 |
| **演示视频**    | 5 分钟完整流程演示（录制中）                               |

### 二、已完成任务清单（Day 1–12）

#### Day 1–3：基础认知 + API 调通

| Day  | 日期 | 任务                        | 关键产出                                          | 状态 |
| :--- | :--- | :-------------------------- | :------------------------------------------------ | :--- |
| 1    | 7/6  | 模型对比 + GitHub 初始化    | `model_comparison.md`，选定 DeepSeek+GLM-5.2      | ✅    |
| 2    | 7/7  | Python 环境 + API 调通      | `first_call.py` 双模型跑通                        | ✅    |
| 3    | 7/8  | Function Calling + 工具定义 | `check_supplier_risk` + `second_call.py` 性能对比 | ✅    |

#### Day 4–7：LangGraph 骨架搭建

| Day  | 日期 | 任务                     | 关键产出                   | 状态 |
| :--- | :--- | :----------------------- | :------------------------- | :--- |
| 4    | 7/9  | LangGraph 核心概念学习   | Quickstart 跑通            | ✅    |
| 5    | 7/10 | 定义 `OrderState` Schema | `graph/state.py`           | ✅    |
| 6    | 7/11 | 组装完整 Agent 图        | 3 节点串连，条件边路由跑通 | ✅    |
| 7    | 7/12 | Week 1 复盘              | `week1_review.md`          | ✅    |

#### Day 8–12：工程化增强 + 交付

| Day  | 日期 | 任务                      | 关键产出                              | 状态 |
| :--- | :--- | :------------------------ | :------------------------------------ | :--- |
| 8    | 7/13 | LangGraph Quickstart 实践 | `test_quickstart.py` + `OrderState`   | ✅    |
| 9    | 7/14 | Excel 解析器 + 统一接口   | `excel_parser.py` + `order_loader.py` | ✅    |
| 10   | 7/15 | PDF 解析器 + 批量轮询     | `pdf_parser.py` + 双文件跑通          | ✅    |
| 11   | 7/15 | 记忆 + 人工复核           | `MemorySaver` + `thread_id`           | ✅    |
| 12   | 7/15 | 工程化收尾                | Rich 表格 + 错误处理                  | ✅    |

### 三、技术亮点

#### 3.1 多格式文件统一输入

- **Excel 解析**：`pandas + openpyxl`，支持中英文列名自动识别，兼容空格和不可见字符
- **PDF 解析**：`pdfplumber`，支持中文合同文本提取 + 正则结构化字段抽取（合同编号、供应商名称、交付日期）
- **统一入口**：根据文件扩展名自动路由到对应解析器

```python
def load_order(file_path: str) -> dict:
    suffix = Path(file_path).suffix.lower()
    if suffix in [".xlsx", ".xls"]:
        return parse_excel_order(file_path)
    elif suffix == ".pdf":
        return parse_pdf_contract(file_path)
```



#### 3.2 LangGraph 状态图设计

- **State**：`OrderState` 承载订单原始数据、风险评分、供应商核验结果、最终决策
- **Node**：`parse_order` → `risk_analysis` → `supplier_verify`
- **Conditional Edge**：根据 `risk_level` 动态路由至 `auto_approve` 或 `human_review`

#### 3.3 记忆 + 人工复核（人机协同）

- `MemorySaver` + `thread_id` 实现多轮对话记忆
- `human_review` 节点通过 `input()` 暂停等待人工决策，输入后恢复执行
- 为后续 Checkpointer 完整实现打下基础

#### 3.4 工程化输出

- `rich` 表格美化审核报告
- 驳回状态红色 Panel 提示，通过状态绿色 Panel
- 全局错误处理（文件不存在、解析失败等）

### 四、踩坑记录（按严重程度排序）

| 坑点                                        | 错误现象                                                     | 根因                      | 解决方案                                                     | 严重程度 |
| :------------------------------------------ | :----------------------------------------------------------- | :------------------------ | :----------------------------------------------------------- | :------- |
| **坑1：LangGraph 导入路径**                 | `ImportError: cannot import name 'StateGraph'`               | 包结构理解错误            | `from langgraph.graph import StateGraph, START, END`         | 🔴 高     |
| **坑2：Excel 列名匹配失败**                 | `supplier_name` 返回 `"supplier_name"` 本身                  | 列名含不可见空格或 BOM 头 | `df.columns.str.strip()` + `row.get(col)` 不依赖 `in`        | 🔴 高     |
| **坑3：`extra_body` 参数位置**              | `UserWarning: Parameters {'extra_body'} should be specified explicitly` | 旧版写法在新版不推荐      | 将 `model_kwargs={"extra_body": {...}}` 改为 `extra_body={...}` | 🟡 中     |
| **坑4：PDF 中文无法渲染**                   | `reportlab` 生成中文 PDF 报错                                | 默认字体不支持中文        | 注册系统中文字体（`simsun.ttc` / `PingFang.ttc`）            | 🟡 中     |
| **坑5：`requires_human_review` 未被消费**   | 字段写入了但未被任何逻辑读取                                 | 设计遗留                  | 用 `final_decision` 替代判断，或直接删除                     | 🟡 中     |
| **坑6：`add_conditional_edges` 映射值类型** | `TypeError: Expected str, got function`                      | 使用了函数对象而非字符串  | `{"auto_approve": "auto_approve"}`（字符串）                 | 🟡 中     |
| **坑7：`reasoning_effort` 参数透传**        | `unexpected keyword argument 'thinking'`                     | `openai` 库版本不支持     | 通过 `extra_body` 透传                                       | 🟢 低     |

### 五、技术决策记录

| 决策点           | 选项                           | 选择                                         | 理由                         |
| :--------------- | :----------------------------- | :------------------------------------------- | :--------------------------- |
| **主力模型**     | Claude / Kimi / DeepSeek / GLM | DeepSeek V4 Flash + GLM-5.2                  | **成本低** + 推理强 + 中文好 |
| **推理强度**     | low / medium / high            | **调试期 medium，演示期 high**               | 平衡成本与效果               |
| **深度思考**     | enabled / disabled             | **始终 enabled**                             | 合同分析需深度推理           |
| **状态管理**     | 顶层字段 vs 嵌套字典           | **顶层 `risk_level` + `supplier_risk_data`** | 便于条件边读取               |
| **人工复核实现** | Checkpointer vs `input()`      | **先用 `input()` 模拟**                      | 快速演示，降低复杂度         |

### 六、项目结构（最终形态）

text

```
ai-pm-learning-journey-main/
├── docs/
│   └──（你的文档 .md）
├── graph/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── agent.py
│   ├── LangGraph/
│   ├── llm_client.py
│   ├── nodes.py
│   └── state.py
├── images/
├── scripts/
│   ├── __init__.py
│   ├── first_call.py
│   └── second_call.py
├── tools/
│   ├── __pycache__/
│   ├── __init__.py
│   └── supplier_risk_check.py
├── utils/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── excel_parser.py
│   ├── order_loader.py
│   └── pdf_parser.py
├── venv_ai/（虚拟环境，不提交）
├── .env
├── .gitignore
├── create_mock_excel.py
├── create_mock_pdf.py
├── LICENSE
├── mock_contract.pdf
├── mock_order.xlsx
├── README.md
├── run_agent.py
└── test_quickstart.py
```



### 七、学习心得

1. **LangGraph 的本质**
   不是“让 LLM 更聪明”，而是“让 LLM 按预定流程执行”。图结构带来的**可控性 > 纯 Prompt 驱动**。
2. **结构化输入是关键**
   PDF 解析的难度远大于 Excel，真实场景中应尽量推动业务方提供结构化数据。
3. **人机协同的工程实现**
   `Checkpointer` + `thread_id` 是实现“暂停-恢复”的标准模式，比 `input()` 阻塞更优雅，适合生产环境。
4. **工程师的“完成标准”**
   代码跑通只是第一步，**错误处理 + 输出美化 + 文档**才是交付的完整形态。
5. **模型选型要基于实测**
   DeepSeek V4 Flash 在速度（第二次调用 6.3s vs GLM 18.16s）和成本上完胜，但 GLM-5.2 在回答深度上略胜。**双主力策略**最灵活。
6. **动态调整比死守计划更重要**
   原计划 Day 4–7 因环境问题顺延，但通过集中攻关（7/15 一天完成 Day 10–12），成功追回进度。

### 八、下一步计划（Day 15–21）

| Day  | 日期 | 任务                            | 目标                               |
| :--- | :--- | :------------------------------ | :--------------------------------- |
| 15   | 7/18 | MCP 协议入门                    | 理解 Server / Tool / Resource 概念 |
| 16   | 7/19 | 搭建 MCP Server 骨架            | `mcp_server/` 基础代码             |
| 17   | 7/20 | 物流查询 MCP Server（mock API） | 与 Claude Desktop 联动             |
| 18   | 7/21 | 多 Agent 协同（CrewAI）入门     | 拆解审核+风控+异常架构             |
| 19   | 7/22 | 三 Agent 协同实现               | 协同跑通                           |
| 20   | 7/23 | 集成测试 + 调试                 | 打 tag `v2.0-beta`                 |
| 21   | 7/24 | 阶段一整体复盘                  | `phase1_review.md`                 |

### 九、关键数据快照

| 指标           | 数据                                                  |
| :------------- | :---------------------------------------------------- |
| 总投入时长     | 约 36–40 小时                                         |
| Python 文件数  | 15+                                                   |
| 核心代码行数   | 约 800+ 行                                            |
| GitHub Commits | 15+                                                   |
| 文档产出       | 6 篇 Markdown                                         |
| 测试文件       | Excel + PDF 双格式                                    |
| 模型对比轮次   | 5 款模型（ChatGPT / Claude / Kimi / 智谱 / DeepSeek） |
| 性能测试数据   | DeepSeek 总耗时 12.63s vs GLM 24.29s                  |

### 十、附录：关键代码片段参考

#### A. LangGraph 条件边（动态路由）

python

```
def route_after_verify(state: OrderState) -> Literal["auto_approve", "human_review"]:
    risk_data = state.get("supplier_risk_data", {})
    risk_level = risk_data.get("risk_level", "低风险")
    return "human_review" if risk_level == "高风险" else "auto_approve"

graph_builder.add_conditional_edges(
    "supplier_verify",
    route_after_verify,
    {"auto_approve": "auto_approve", "human_review": "human_review"}
)
```



#### B. MemorySaver 记忆

python

```
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
agent = graph_builder.compile(checkpointer=memory)

# 运行时传入 thread_id
config = {"configurable": {"thread_id": "order-mock_contract"}}
final_state = agent.invoke(initial_state, config=config)
```



#### C. DeepSeek 深度思考配置

python

```
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.3,
    extra_body={
        "thinking": {"type": "enabled"},
        "reasoning_effort": "medium"
    }
)
```



### 十一、总结

**Day 1–12 完成了一个完整的 Agent 从 0 到 1 的构建闭环**：

1. ✅ **选型**：5 款模型对比 → 选定 DeepSeek + GLM-5.2 双主力
2. ✅ **验证**：API 调通 → Function Calling 工具调用
3. ✅ **骨架**：LangGraph 状态图 → 3 节点 + 条件边
4. ✅ **输入**：Excel + PDF 双格式解析 → 批量轮询
5. ✅ **增强**：记忆（MemorySaver）+ 人工复核
6. ✅ **交付**：Rich 表格 + 错误处理 + 5 分钟演示视频

**当前能力状态**：Agent 已能自动读取 Excel/PDF 采购文件，调用大模型分析风险，结合供应商数据做出自动通过或转人工复核的决策，支持多轮记忆和人工干预，输出专业美观的审核报告