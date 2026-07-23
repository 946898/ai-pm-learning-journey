# 阶段一复盘总结（Day 1–19）：基础搭建

> **复盘日期**：2026-07-23  
> **阶段目标**：从 0 到 1 搭建可用的采购订单智能审核 Agent 原型  
> **总投入**：约 48 小时（工作日 2h/天，周末 5h/天）  
> **版本状态**：✅ tag `v2.0-beta`


## 一、阶段概览

| 维度 | 内容 |
| :--- | :--- |
| **阶段范围** | Day 1–19（2026-07-06 至 2026-07-23） |
| **核心目标** | 搭建可用的 Agent 原型，掌握 LangGraph、MCP、多 Agent 协同 |
| **最终产出** | 采购订单智能审核 Agent v2.0-beta（支持 Excel/PDF 输入 + 记忆 + 人工复核 + MCP 工具 + 多 Agent 协同） |
| **代码量** | 15+ Python 文件，约 1200+ 行核心代码 |
| **GitHub Commits** | 25+ |


## 二、技术成果

### 2.1 LangGraph Agent（Day 4–6）

| 组件 | 实现 | 文件 |
| :--- | :--- | :--- |
| **状态定义** | `OrderState`：订单原始数据 + 风险评分 + 供应商核验结果 + 最终决策 | `graph/state.py` |
| **三个节点** | `parse_order` → `risk_analysis` → `supplier_verify` | `graph/nodes.py` |
| **条件路由** | `route_after_verify`：高风险 → 人工复核，低/中风险 → 自动通过 | `graph/agent.py` |
| **记忆** | `MemorySaver` + `thread_id` 实现多轮对话记忆 | `graph/agent.py` |

**关键决策**：使用 LangGraph 而非 LangChain Chain，因为图结构对分支逻辑和条件路由的支持更好。

### 2.2 多格式输入（Day 8–10）

| 格式 | 解析方式 | 特点 |
| :--- | :--- | :--- |
| **Excel** | `pandas + openpyxl` | 支持中英文列名自动识别 |
| **PDF** | `pdfplumber` | 支持中文合同文本提取 + 正则结构化字段抽取 |
| **统一接口** | `load_order(file_path)` | 根据扩展名自动路由 |

**关键决策**：优先支持结构化输入（Excel），再扩展非结构化（PDF）。

### 2.3 记忆 + 人工复核（Day 11）

| 功能 | 实现 | 文件 |
| :--- | :--- | :--- |
| **记忆** | `MemorySaver` + `thread_id` | `graph/agent.py` |
| **人工复核** | `human_review` 节点通过 `input()` 暂停等待人工决策 | `graph/agent.py` |

**关键决策**：用 `input()` 模拟人工复核，保持实现简单，未来可升级为 Webhook。

### 2.4 MCP Server（Day 15–17）

| 组件 | 实现 | 文件 |
| :--- | :--- | :--- |
| **MCP Server** | `add_request_handler` 处理 `tools/list` 和 `tools/call` | `mcp_server/supplier_server.py` |
| **工具包装** | 将 `check_supplier_risk` 包装为 MCP Tool | `mcp_server/supplier_server.py` |
| **客户端集成** | Cline 配置 MCP Server，成功调用工具 | `docs/mcp_config.md` |

**关键决策**：使用 `add_request_handler` 而非高层装饰器，因为 `mcp==2.0.0b1` 版本更稳定。

### 2.5 多 Agent 协同（Day 18–19）

| Agent | 角色 | 工具 |
| :--- | :--- | :--- |
| **审核 Agent** | 解析采购订单信息 | 无 |
| **风控 Agent** | 评估供应商履约风险 | `check_supplier_risk` |
| **异常 Agent** | 生成高风险订单的处理建议 | 无 |

**关键决策**：三 Agent 顺序执行（sequential），保证数据流转清晰可控。

### 2.6 工程化 + 评测（Day 12 + 规划中）

| 功能 | 实现 | 状态 |
| :--- | :--- | :--- |
| **输出美化** | Rich 表格 + 红绿 Panel | ✅ |
| **错误处理** | 文件不存在、解析失败友好提示 | ✅ |
| **评测方案** | 20 个测试用例 + 评分标准 + 发布门禁 | ⏳ 周末完成 |


## 三、踩坑记录

### 3.1 LangGraph 相关

| 问题 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| `ImportError: cannot import name 'StateGraph'` | 包结构理解错误 | `from langgraph.graph import StateGraph, START, END` |
| `add_conditional_edges` 映射值类型错误 | 使用了函数对象而非字符串 | `{"auto_approve": "auto_approve"}`（字符串） |

### 3.2 输入解析相关

| 问题 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| `supplier_name` 返回 `"supplier_name"` 本身 | Excel 列名含不可见空格 | `df.columns.str.strip()` + `row.get(col)` 不依赖 `in` |
| PDF 中文无法渲染 | `reportlab` 默认不支持中文 | 注册系统中文字体（`simsun.ttc`） |

### 3.3 MCP 相关

| 问题 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'mcp.types'` | 版本差异，`mcp==2.0.0b1` 中 `types` 在顶层 | `from mcp import Tool` 而非 `from mcp.types import Tool` |
| `add_request_handler` 报错 | 参数顺序错误 | `add_request_handler(method, params_type, handler)` |
| `capabilities` 缺失 | `InitializationOptions` 需要明确声明 | `capabilities=server.get_capabilities()` |

### 3.4 CrewAI 相关

| 问题 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| `OPENAI_API_KEY is required` | CrewAI 默认使用 OpenAI | 通过 `LLM` 类配置 DeepSeek |
| `OpenAI function name cannot be empty` | 工具名称未正确传递 | `@tool("check_supplier_risk")` 明确指定名称 |
| Agent 不调用工具 | Task description 未明确要求 | 在 Task 描述中强调“必须调用工具” |


## 四、数据快照

| 指标 | 数据 |
| :--- | :--- |
| 总投入时长 | 约 48 小时 |
| Python 文件数 | 15+ |
| 核心代码行数 | 约 1200+ 行 |
| GitHub Commits | 25+ |
| 文档产出 | 7 篇 Markdown |
| 测试文件 | Excel + PDF 双格式 |
| 模型对比轮次 | 5 款模型（ChatGPT / Claude / Kimi / 智谱 / DeepSeek） |
| MCP 工具数 | 1 个（`check_supplier_risk`） |
| CrewAI Agent 数 | 3 个（审核 / 风控 / 异常） |
| 版本 Tag | `v2.0-beta` |


## 五、学习心得

### 5.1 技术层面

1. **LangGraph 的本质**：不是“让 LLM 更聪明”，而是“让 LLM 按预定流程执行”。图结构带来的可控性 > 纯 Prompt 驱动。
2. **结构化输入是关键**：PDF 解析的难度远大于 Excel，真实场景中应尽量推动业务方提供结构化数据。
3. **MCP 协议的价值**：标准化 Agent 与外部工具的通信方式，避免每个模型、每个客户端都要定制接口。
4. **多 Agent vs 单 Agent**：分工明确的多个 Agent（审核 + 风控 + 异常）比一个全能 Agent 更容易调试、更可控、更可观测。

### 5.2 产品层面

1. **评测是 AI 产品的“测试”**：传统产品测试是验证功能正确，AI 产品评测是持续监测能力是否退化。
2. **人机协同是必须的**：高风险订单转人工复核不仅是“兜底”，更是用户建立信任的关键机制。
3. **版本管理是 AI 工程的刚需**：不同版本的 Prompt、工具、工作流会产生截然不同的效果，必须用 Git + Tag 管理。

### 5.3 工程层面

1. **先跑通再优化**：Day 1–3 先跑通 API，Day 4–6 先跑通骨架，Day 8–10 先跑通输入，逐步迭代。
2. **错误处理 + 输出美化 = 交付物**：代码跑通只是第一步，工程化收尾才是可交付的形态。
3. **版本 Tag 是里程碑**：每个关键节点打一个 Tag，方便回溯和面试展示。


## 六、下一步计划

### 6.1 短期（Day 20–21）

| 任务 | 说明 | 状态 |
| :--- | :--- | :--- |
| 阶段一复盘 | 完成 `phase1_review.md` | ✅ 进行中 |
| 评测方案落地 | 建立 20 个测试用例 + 评分标准 | ⏳ 周末完成 |
| 休息/缓冲 | 回顾前期学习，整理笔记 | ⏳ 待开始 |

### 6.2 中期（Day 22–48）

| 阶段 | 任务 | 交付物 |
| :--- | :--- | :--- |
| **阶段二：行业落地** | 案例拆解 + 深做 Demo + 深度分析文章 | 3 篇拆解文章 + Docker 镜像 + 3000 字深度分析 |


## 七、关键命令速查

```bash
# LangGraph Agent 运行
python run_agent.py

# CrewAI 多 Agent 协同运行
python -m crew.run_crew

# MCP Server 启动
python -m mcp_server.supplier_server

# 评测运行
python eval_agent.py

# 打 tag
git tag -a v2.0-beta -m "v2.0-beta: multi-agent crew with tool calling"
git push origin v2.0-beta