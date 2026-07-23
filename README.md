## 📅 AI 产品经理转型计划 —— 天级任务清单（倒序排列）

> **起始日期**：2026-07-06（Day 1）  
> **当前进度**：已完成 Day 1–19  
> **预计截止**：2026-09-13（Day 70）


### 一、已完成任务（倒序：从最近到最远）

| Day | 日期 | 实际完成内容 | 交付物 | 状态 |
| :---: | :--- | :--- | :--- | :---: |
| 19 | 7/23（周四） | 集成测试 + 调试 + 打 tag | 三 Agent 协同完整跑通，打 tag `v2.0-beta` | ✅ |
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


### 二、阶段一完成（Day 1–19）

**阶段目标**：搭建可用的 Agent 原型

| 里程碑 | 交付物 | 状态 |
| :--- | :--- | :---: |
| 模型选型 + API 调通 | `model_comparison.md` + `first_call.py` | ✅ |
| Function Calling | `check_supplier_risk` + `second_call.py` | ✅ |
| LangGraph 骨架 | 3 节点 + 条件边 + 状态图 | ✅ |
| Excel/PDF 输入接入 | `excel_parser.py` + `pdf_parser.py` | ✅ |
| 记忆 + 人工复核 | `MemorySaver` + `thread_id` | ✅ |
| 工程化收尾 | Rich 表格 + 错误处理 | ✅ |
| MCP Server 开发 | `mcp_server/supplier_server.py` | ✅ |
| MCP + Cline 集成 | Cline 工具调用成功 | ✅ |
| 多 Agent 协同 | `crew/` 三 Agent 工作流 | ✅ |
| 版本发布 | tag `v2.0-beta` | ✅ |


### 三、待完成任务（Day 20–70）

#### 阶段一收尾 + 缓冲

| Day | 日期 | 任务 | 交付物 |
| :---: | :--- | :--- | :--- |
| 20 | 7/24（周五） | 阶段一整体复盘 + 休息/缓冲 | `phase1_review.md` |

#### 阶段二：行业落地（Day 21–56）

| Day | 日期 | 任务 | 交付物 |
| :---: | :--- | :--- | :--- |
| 21–22 | 7/25–7/26 | 案例拆解①：快递 100「果宝」 | 第 1 篇拆解文章（1500 字） |
| 23–24 | 7/27–7/28 | 案例拆解②：京东「物流超脑」 | 第 2 篇拆解文章 |
| 25–26 | 7/29–7/30 | 案例拆解③：讯飞招采智能体 | 第 3 篇拆解文章 |
| 27 | 7/31 | 三案例对比总结 | 1 篇对比总结 |
| 28–32 | 8/1–8/5 | 深做 Demo v2 工程化 | Docker 镜像 + 日志 + 重试 |
| 33–34 | 8/6–8/7 | 10 分钟演示视频 | 视频录制 + README 更新 |
| 35–37 | 8/8–8/10 | 撰写深度分析文章（3000 字） | 文章初稿 |
| 38 | 8/11 | 文章投递 | 投递 36 氪/脉脉 |
| 39–48 | 8/12–8/21 | 缓冲/补充 + 阶段二复盘 | `phase2_review.md` |

#### 后续阶段（Day 49–70）

| Day | 日期 | 任务 | 交付物 |
| :---: | :--- | :--- | :--- |
| 49–56 | 8/22–8/29 | 按需规划 | 根据前两阶段成果决定 |
| 57–70 | 8/30–9/13 | 最终交付物整理 | 完整作品集归档 |

### 四、Demo_video_link

#### 采购订单审核 agent_demo：

https://www.bilibili.com/video/BV1hPKV6zERx/


### 五、配套说明

- **每日反馈**：每晚告知当日进展，我会在次日早上定制具体任务。
- **每 7 天复盘**：总结产出、踩坑和下一步计划。
- **GitHub 持续更新**：所有代码、文档、文章托管在 GitHub。
- **后续阶段灵活调整**：根据实际进度和兴趣点动态调整。