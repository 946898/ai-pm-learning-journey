## 更新后的周级路线图

### 一、整体进度总览

| 阶段         | 周次  | 日期      | 核心目标                                                | 状态                |
| :----------- | :---- | :-------- | :------------------------------------------------------ | :------------------ |
| **基础搭建** | W1    | 7/6–7/12  | 模型选型 + API 调通 + Function Calling + LangGraph 骨架 | ✅ 已完成            |
|              | W2    | 7/13–7/19 | Excel/PDF 输入 + 记忆 + 人工复核 + 工程化收尾           | ✅ 已完成（Day8–12） |
|              | W3    | 7/20–7/26 | MCP 协议入门 + 物流查询 MCP Server                      | ⏳ 待开始            |
|              | W4    | 7/27–8/2  | 多 Agent 协同（CrewAI） + v2 架构改造                   | ⏳ 待开始            |
| **行业落地** | W5–W8 | 8/3–8/30  | 案例拆解 + 深做 Demo v2 + 深度分析文章                  | ⏳ 待开始            |

------

## 二、W1 完成内容（7/6–7/12）

| Day  | 任务                        | 关键产出                                                     | 状态 |
| :--- | :-------------------------- | :----------------------------------------------------------- | :--- |
| 1    | 模型对比 + GitHub 初始化    | `docs/model_comparison.md`，选定 DeepSeek+GLM-5.2            | ✅    |
| 2    | Python 环境 + API 调通      | `scripts/first_call.py` 双模型跑通                           | ✅    |
| 3    | Function Calling + 工具定义 | `tools/supplier_risk_check.py` + `scripts/second_call.py` 性能对比 | ✅    |
| 4    | LangGraph 核心概念学习      | Quickstart 跑通                                              | ✅    |
| 5    | 定义 `OrderState` Schema    | `graph/state.py`                                             | ✅    |
| 6    | 组装 Agent 图               | 3 节点串连，条件边路由跑通                                   | ✅    |
| 7    | Week 1 复盘                 | `docs/week1_review.md`                                       | ✅    |

------

## 三、W2 完成内容（7/13–7/15）

| Day  | 任务                      | 关键产出                                          | 状态 |
| :--- | :------------------------ | :------------------------------------------------ | :--- |
| 8    | LangGraph Quickstart 实践 | `test_quickstart.py` + `graph/` 核心文件          | ✅    |
| 9    | Excel 解析器 + 统一接口   | `utils/excel_parser.py` + `utils/order_loader.py` | ✅    |
| 10   | PDF 解析器 + 批量轮询     | `utils/pdf_parser.py` + 双文件跑通                | ✅    |
| 11   | 记忆 + 人工复核           | `graph/agent.py` 集成 `MemorySaver` + `thread_id` | ✅    |
| 12   | 工程化收尾                | Rich 表格 + 错误处理 + 驳回红色 Panel             | ✅    |

------

## 四、当前项目文件与功能映射

| 文件/目录                      | 对应功能                                            |
| :----------------------------- | :-------------------------------------------------- |
| `graph/agent.py`               | 主图编译 + MemorySaver + 路由逻辑                   |
| `graph/state.py`               | `OrderState` 状态定义                               |
| `graph/nodes.py`               | `parse_order` / `risk_analysis` / `supplier_verify` |
| `graph/llm_client.py`          | DeepSeek LLM 配置（含 thinking + reasoning_effort） |
| `utils/excel_parser.py`        | Excel 解析（中英文列名兼容）                        |
| `utils/pdf_parser.py`          | PDF 解析（中文 + 正则提取编号/供应商/金额）         |
| `utils/order_loader.py`        | 统一输入接口（根据扩展名路由）                      |
| `tools/supplier_risk_check.py` | 供应商风险 Mock 数据                                |
| `run_agent.py`                 | 入口脚本（批量轮询 + Rich 表格）                    |
| `scripts/first_call.py`        | Day 2 模型 API 调通验证                             |
| `scripts/second_call.py`       | Day 3 Function Calling 性能对比                     |
| `test_quickstart.py`           | LangGraph Quickstart 验证                           |

------

## 五、待启动模块（W3–W8）

| 周次  | 新增任务                   | 新增文件（规划）                        |
| :---- | :------------------------- | :-------------------------------------- |
| W3    | MCP 协议入门 + Server 搭建 | `mcp_server/` 目录                      |
| W4    | 多 Agent 协同（CrewAI）    | `crew/` 目录（或 `graph/multi_agent/`） |
| W5–W6 | 案例拆解文章               | `docs/case_study_*.md`                  |
| W7    | 深做 Demo v2               | `docker/` + 日志/重试增强               |
| W8    | 深度分析文章               | `docs/deep_analysis.md`                 |

------

## 六、下一步行动（Day 15–21）

| Day  | 日期 | 任务                            | 产出                    |
| :--- | :--- | :------------------------------ | :---------------------- |
| 15   | 7/18 | MCP 协议入门 + 环境搭建         | MCP 概念笔记            |
| 16   | 7/19 | 搭建 MCP Server 骨架            | `mcp_server/` 基础代码  |
| 17   | 7/20 | 物流查询 MCP Server（mock API） | 与 Claude Desktop 联动  |
| 18   | 7/21 | 多 Agent 协同（CrewAI）入门     | 架构设计文档            |
| 19   | 7/22 | 三 Agent 协同实现               | 协同跑通                |
| 20   | 7/23 | 集成测试 + 调试                 | 打 tag `v2.0-beta`      |
| 21   | 7/24 | 阶段一整体复盘                  | `docs/phase1_review.md` |