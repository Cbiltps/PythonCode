from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 确保 OPENAI_API_KEY 已设置
print("--- 2.1 LLM 与 Chat Model 接口演示 ---")

# 初始化一个 ChatModel - 推荐使用 gpt-3.5-turbo 或 gpt-4
# temperature 控制模型生成文本的随机性，0 表示确定性最高，1 表示创造性最高。
chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 场景一：简单的用户提问
print("\n--- 场景一：简单的用户提问 ---")
user_query = "你好，请用一句话介绍一下 Langchain。"
response = chat_model.invoke([HumanMessage(content=user_query)])
print(f"用户提问: {user_query}")
print(
    f"ChatModel 响应: {response.content}"
)  # response 是 AIMessage 对象，内容在 .content 属性中

# 场景二：结合系统消息，为模型设定角色或行为
print("\n--- 场景二：结合系统消息，为模型设定角色或行为 ---")
messages_with_system = [
    SystemMessage(content="你是一个专业的编程语言导师，擅长简洁明了地解释概念。"),
    HumanMessage(content="请解释一下 Python 中的装饰器。"),
]
response_system_role = chat_model.invoke(messages_with_system)
print(f"设定角色后 ChatModel 响应: {response_system_role.content}")

# 场景三：模拟多轮对话的结构（实际应用中会结合 Memory 模块）
print("\n--- 场景三：模拟多轮对话结构 ---")
# 这里的 messages 列表代表了对话历史
dialog_history = [
    HumanMessage(content="我最喜欢的编程语言是 Python。"),
    AIMessage(content="Python 是一个非常流行的语言！你喜欢它的哪些特性呢？"),
    HumanMessage(content="我喜欢它的简洁性和丰富的库生态。"),
]
response_multi_turn = chat_model.invoke(dialog_history)
print(f"ChatModel 响应 (模拟多轮): {response_multi_turn.content}")
