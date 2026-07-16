# Week 2 复盘（Day 8–12）

> **时间**：7/13 – 7/15  
> **核心目标**：Agent 工程化（Excel/PDF 输入 + 记忆 + 人工复核）

## 一、已完成任务
- Day 8：LangGraph 核心概念 + State Schema
- Day 9：Excel 解析器 + 统一输入接口
- Day 10：PDF 解析器 + 批量轮询
- Day 11：记忆（MemorySaver）+ 人工复核
- Day 12：工程化收尾（Rich 表格 + 错误处理）

## 二、技术亮点
1. **多格式输入**：统一接口支持 `.xlsx` / `.pdf`，自动路由解析。
2. **人机协同**：高风险订单自动暂停，等待人工输入后继续。
3. **工程化输出**：Rich 表格美化 + 驳回红色警告。

## 三、踩坑记录
- LangGraph 导入路径问题：`StateGraph` 需从 `langgraph.graph` 导入。
- Excel 列名匹配失败：用 `row.get()` 直接取值，避免 `in` 判断受不可见字符干扰。
- PDF 中文渲染：需注册系统中文字体（`simsun.ttc`）。
- `requires_human_review` 字段未被使用，最终改用 `final_decision` 判断。

## 四、后续计划
- Day 15 开始 MCP 协议实战。