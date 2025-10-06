from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

print("\n--- 2.2 Prompt Templates 演示 ---")

# 初始化一个 ChatModel - 推荐使用 gpt-3.5-turbo 或 gpt-4
# temperature 控制模型生成文本的随机性，0 表示确定性最高，1 表示创造性最高。
chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 1. 使用 PromptTemplate (适用于旧式LLM，了解即可)
# 作用：将输入变量填充到模板字符串中
poem_template = PromptTemplate(
    input_variables=["topic", "style"],
    template="请给我写一首关于 {topic} 的诗歌，风格是 {style}。",
)

# 格式化 Prompt，传入变量
formatted_poem_prompt = poem_template.format(topic="秋天的落叶", style="伤感")
print(f"格式化后的 Prompt (PromptTemplate):\n{formatted_poem_prompt}")

# 2. 使用 ChatPromptTemplate (推荐，适用于 ChatModel)
# 作用：构建结构化的消息列表，每个消息可以有自己的模板
coding_assistant_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="你是一个经验丰富的Python程序员，擅长解答编程问题，并给出代码示例。"
        ),
        HumanMessage(content="请用 {language} 语言，实现一个 {functionality} 的函数。"),
    ]
)

# 格式化 ChatPromptTemplate，传入变量，返回一个消息对象列表
messages_for_coding = coding_assistant_template.format_messages(
    language="Python", functionality="计算斐波那契数列的第 n 项"
)

print("\n格式化后的 Chat Messages (ChatPromptTemplate):")
for msg in messages_for_coding:
    print(f"  {type(msg).__name__}: {msg.content[:50]}...")  # 打印部分内容

# 将格式化后的消息发送给 ChatModel
# chat_model 在 2.1 节已初始化
response_code = chat_model.invoke(messages_for_coding)
print(f"\nChatModel 生成的代码解释:\n{response_code.content[:300]}...")  # 打印部分响应

# 另一个更复杂的 ChatPromptTemplate 示例：需要JSON格式输出
json_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="你是一个数据提取专家，请将用户信息提取为 JSON 格式。"),
        HumanMessage(
            content="请从以下文本中提取用户的姓名和年龄：\n\n用户资料：我叫李明，今年28岁。"
        ),
        HumanMessage(
            content='请确保输出为严格的 JSON 格式，例如: `{{"name": "", "age": 0}}`'
        ),
    ]
)

json_messages = json_prompt.format_messages()  # 无需额外变量，直接格式化
response_json = chat_model.invoke(json_messages)
print(f"\nChatModel 生成的 JSON:\n{response_json.content}")
