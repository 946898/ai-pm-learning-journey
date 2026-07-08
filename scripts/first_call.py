# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# # 加载 .env 文件中的环境变量
# load_dotenv()

# # ========== 1. DeepSeek 专家模式 ==========
# print("=== DeepSeek V4-flash模式 (deepseek-v4-flash) ===")
# client_ds = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com"
# )

# try:
#     response_ds = client_ds.chat.completions.create(
#         model="deepseek-v4-flash",
#         messages=[
#             {"role": "system", "content": "你是一位资深的采购合同风险管理专家。"},
#             {"role": "user", "content": "请评估一份采购合同中'逾期交货违约金'条款的风险，给出3条修改建议。"}
#         ],
#         temperature=0.3,
#         stream=False,
#         reasoning_effort="medium",
#         extra_body={"thinking": {"type": "enabled"}}
#     )
#     print(response_ds.choices[0].message.content)
# except Exception as e:
#     print(f" DeepSeek 报错: {e}")

# print("\n" + "="*60 + "\n")

# # ========== 2. 智谱 GLM-5.2 ==========
# print("=== 智谱 GLM-5.2 ===")
# client_glm = OpenAI(
#     api_key=os.getenv("GLM_API_KEY"),
#     base_url="https://open.bigmodel.cn/api/paas/v4/"
# )

# try:
#     response_glm = client_glm.chat.completions.create(
#         model="glm-5.2",  # 如果报错，去智谱控制台查精确 model 代号
#         messages=[
#             {"role": "system", "content": "你是一位资深的采购合同风险管理专家。"},
#             {"role": "user", "content": "请评估一份采购合同中'逾期交货违约金'条款的风险，给出3条修改建议。"}
#         ],
#         temperature=0.3,
#     )
#     print(response_glm.choices[0].message.content)
# except Exception as e:
#     print(f" GLM-5.2 报错: {e}")