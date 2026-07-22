## 📅 AI 产品经理转型计划 —— 天级任务清单（倒序排列）

> **起始日期**：2026-07-06（Day 1）  
> **当前进度**：已完成 Day 1–18  
> **预计截止**：2026-09-13（Day 70）


### 一、已完成任务（倒序：从最近到最远）

| Day | 日期 | 实际完成内容 | 交付物 | 状态 |
| :---: | :--- | :--- | :--- | :---: |
| 18 | 7/22（周三） | 多 Agent 协同（CrewAI）三 Agent 工作流 | `crew/` 目录，三 Agent 协同跑通，输出异常处理报告 | ✅ |
| 17 | 7/22（周三） | MCP Server 与 Cline 联动 | Cline 成功调用 `check_supplier_risk` 工具 | ✅ |
| 16 | 7/21（周二） | 搭建 MCP Server 骨架 | `mcp_server/supplier_server.py` 创建并测试通过 | ✅ |
| 15 | 7/20（周一） | MCP 协议环境搭建 + Quickstart 验证 | `mcp_quickstart.py` 跑通，MCP SDK 环境就绪 | ✅ |
| 14 | 7/17（周五） | 缓冲/补漏 | 生成 `requirements.txt`、`.env.example`，修复 `nodes.py` | ✅ |
| 13 | 7/16（周四） | Week 2 复盘 + 5 分钟演示视频 | `week2_review.md` + B站视频链接 | ✅ |
| 12 | 7/15（周三） | 工程化收尾 | Rich 表格美化 + 错误处理 + 驳回红色 Panel | ✅ |
| 11 | 7/15（周三） | 记忆 + 人工复核 | `MemorySaver` + `thread_id` + 人工复核暂停/恢复 | ✅ |
| 10 | 7/15（周三） | PDF 解析器完善 + 批量轮询 | `pdf_parser.py` 支持中文合同提取 + 双文件跑通 | ✅ |
| 9 | 7/14（周二） | Excel 解析器 + 统一接口 | `excel_parser.py` + `order_loader.py` 完成 | ✅ |
| 8 | 7/13（周一） | LangGraph Quickstart 实践 | `test_quickstart.py` 跑通，`OrderState` 定义完成 | ✅ |
| 7 | 7/12（周日） | Week 1 复盘 | `week1_review.md`，README 优化，录屏准备 | ✅ |
| 6 | 7/11（周六） | 组装完整 Agent 图 | 3 节点串连，条件边路由，`auto_approve` / `human_review` 跑通 | ✅ |
| 5 | 7/10（周五） | 定义 `OrderState` Schema | `graph/state.py` 完成，手绘状态流转图 | ✅ |
| 4 | 7/9（周四） | LangGraph 核心概念学习 | Quickstart 阅读 + 概念理解 | ✅ |
| 3 | 7/8（周三） | Function Calling + 工具定义 | `check_supplier_risk` + `second_call.py` 性能对比 | ✅ |
| 2 | 7/7（周二） | Python 环境 + 第一次 API 调用 | `first_call.py` 双模型调通 | ✅ |
| 1 | 7/6（周一） | 模型对比 + GitHub 初始化 | `model_comparison.md`，选定 DeepSeek+GLM-5.2 | ✅ |


### 二、待完成任务（正序：从近到远）

#### 阶段一：基础搭建（Day 19–28）

| Day | 日期 | 任务 | 交付物 |
| :---: | :--- | :--- | :--- |
| 19 | 7/23（周四） | 集成测试 + 调试（三 Agent 联调 + 工具调用修复） | 完整工作流跑通，打 tag `v2.0-beta` |
| 20 | 7/24（周五） | 阶段一整体复盘 | `phase1_review.md` |
| 21–28 | 7/25–8/1 | 缓冲/补充 | 补齐遗漏任务 |

#### 阶段二：行业落地（Day 29–56）

| Day | 日期 | 任务 | 交付物 |
| :---: | :--- | :--- | :--- |
| 29–30 | 8/3–8/4 | 案例拆解①：快递 100「果宝」 | 第 1 篇拆解文章（1500 字） |
| 31–32 | 8/5–8/6 | 案例拆解②：京东「物流超脑」 | 第 2 篇拆解文章 |
| 33–34 | 8/7–8/8 | 案例拆解③：讯飞招采智能体 | 第 3 篇拆解文章 |
| 35 | 8/9 | 三案例对比总结 | 1 篇对比总结 |
| 36–40 | 8/10–8/14 | 深做 Demo v2 工程化 | Docker 镜像 + 日志 + 重试 |
| 41–42 | 8/15–8/16 | 10 分钟演示视频 | 视频录制 + README 更新 |
| 43–45 | 8/17–8/19 | 撰写深度分析文章（3000 字） | 文章初稿 |
| 46 | 8/20 | 文章投递 | 投递 36 氪/脉脉 |
| 47–56 | 8/21–8/30 | 缓冲/补充 + 阶段二复盘 | `phase2_review.md` |

#### 后续阶段（Day 57–70）

| Day | 日期 | 任务 | 交付物 |
| :---: | :--- | :--- | :--- |
| 57–63 | 8/31–9/6 | 按需规划 | 根据前两阶段成果决定 |
| 64–70 | 9/7–9/13 | 最终交付物整理 | 完整作品集归档 |


### 三、关键里程碑（倒序，从最近到最远）

| 里程碑 | 预计 Day | 交付物 | 状态 |
| :--- | :---: | :--- | :---: |
| 多 Agent 协同（CrewAI）工作流跑通 | Day 18 | `crew/` 三 Agent 协作输出异常报告 | ✅ |
| MCP Server 与 Cline 联动成功 | Day 17 | Cline 调用 `check_supplier_risk` | ✅ |
| MCP Server 骨架搭建 | Day 16 | `mcp_server/supplier_server.py` 可启动 | ✅ |
| MCP 环境搭建 + Quickstart 验证 | Day 15 | `mcp_quickstart.py` 跑通 | ✅ |
| 工程化收尾（错误处理 + Rich 表格） | Day 12 | 美化输出 + 错误处理 | ✅ |
| 记忆 + 人工复核 | Day 11 | `MemorySaver` + `thread_id` | ✅ |
| Excel/PDF 输入接入 | Day 8–10 | 双格式解析 + 批量轮询 | ✅ |
| Agent 骨架跑通 | Day 4–6 | LangGraph 图 + 条件边路由 | ✅ |
| 模型选型 + API 调通 | Day 1–3 | `model_comparison.md` + `first_call.py` | ✅ |
| 阶段一完成 | Day 28 | 1 Agent + 1 MCP 工具 + 多 Agent 协同 | ⏳ |
| 阶段二前半完成 | Day 34 | 3 篇案例拆解文章 | ⏳ |
| 阶段二完成 | Day 56 | 深做 Demo v2 + 深度分析文章 | ⏳ |

### 四、Demo_video_link

#### 采购订单审核 agent_demo：

https://www.bilibili.com/video/BV1hPKV6zERx/


### 五、配套说明

- **每日反馈**：每晚告知当日进展，我会在次日早上定制具体任务。
- **每 7 天复盘**：总结产出、踩坑和下一步计划。
- **GitHub 持续更新**：所有代码、文档、文章托管在 GitHub。
- **后续阶段灵活调整**：根据实际进度和兴趣点动态调整。