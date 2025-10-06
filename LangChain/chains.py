from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # 用于将模型输出解析成字符串
from langchain_core.runnables import RunnablePassthrough, Runnable  # 用于传递输入
from langchain_openai import ChatOpenAI

print("\n--- 2.3 LCEL (Chains) 演示 ---")

# 初始化一个 ChatModel - 推荐使用 gpt-3.5-turbo 或 gpt-4
# temperature 控制模型生成文本的随机性，0 表示确定性最高，1 表示创造性最高。
chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 1. 定义 Prompt Template
code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="你是一个专业的 Python 编程助手，擅长清晰地解释概念并提供简洁的代码示例。"
        ),
        HumanMessage(
            content="请为我解释并提供一个关于 Python '{concept}' 的代码示例。"
        ),
        HumanMessage(content="请确保解释和代码都清晰易懂。"),
    ]
)

# 2. 初始化 Chat Model
# chat_model 在 2.1 节已初始化

# 3. 定义输出解析器
# StrOutputParser 会把 ChatModel 返回的 AIMessage 对象中的 .content 部分提取出来
output_parser = StrOutputParser()

# 4. 构建 LCEL 链
# 链的输入是一个字典，例如 {"concept": "装饰器"}
# 1. `code_gen_prompt` 接收 {"concept": "..."}，生成 Chat Messages 列表
# 2. `chat_model` 接收 Chat Messages 列表，返回 AIMessage 对象
# 3. `output_parser` 接收 AIMessage 对象，解析成纯字符串
code_explanation_chain = code_gen_prompt | chat_model | output_parser

# 5. 调用链并传入输入变量
input_concept = "生成器"
print(f"正在生成关于 '{input_concept}' 的代码示例和解释...")
result = code_explanation_chain.invoke({"concept": input_concept})
print(f"\n链的输出:\n{result}")


# 另一个链的例子：先将用户输入转换为英文，再进行解释
# 步骤1：翻译 Prompt
translate_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="你是一个专业的翻译家，将用户输入的中文短语翻译成英文。"),
        HumanMessage(content="请将 '{text}' 翻译成英文。"),
    ]
)

# 步骤2：英文解释 Prompt
explain_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="你是一个专业词汇解释器，用简洁的英文解释词语。"),
        HumanMessage(content="请解释一下 '{english_text}' 这个词汇的含义。"),
    ]
)

# 构建一个更复杂的链：
# 1. 接收一个包含 "text" 的字典，例如 {"text": "并行计算"}
# 2. 通过 RunnablePassthrough 将 "text" 传给 translate_prompt
# 3. translate_chain 翻译中文到英文，其输出是英文文本
# 4. assign() 将翻译结果添加到字典中，键为 "english_text"
# 5. explain_prompt 接收 "english_text"，生成解释 Prompt
# 6. chat_model 和 output_parser 处理最终的解释
translation_and_explanation_chain = (
    {"text": RunnablePassthrough()}  # type: ignore # 接收原始输入并传递
    | translate_prompt
    | chat_model
    | output_parser.assign(english_text=lambda x: x)  # 将翻译结果赋值给 english_text 键
    | explain_prompt
    | chat_model
    | output_parser
)

# 注意：上面的 .assign() 只是一个示意，实际复杂的链可能需要更精妙的 RunnableParallel/RunnableMap 来处理多输入
# 这里简化为串行处理，只传递一个主要输入。

# 假设我们需要一个更清晰的多步骤链，来演示输入传递
# Step 1: 翻译
translator_chain = translate_prompt | chat_model | output_parser

# Step 2: 解释 (需要上一步的翻译结果)
# 这里的{"english_text": translator_chain} 表示将 translator_chain 的输出作为 english_text 的值
full_pipeline = (
    {   # type: ignore
        "english_text": translator_chain,
        "original_text": RunnablePassthrough()  # 传递原始的 "text" 输入，供后续步骤使用（如果需要）
    }
    | explain_prompt
    | chat_model
    | output_parser
)

input_text_for_pipeline = "并发编程"
print(f"\n正在处理概念：'{input_text_for_pipeline}'")
explanation_result = full_pipeline.invoke({"text": input_text_for_pipeline})
print(f"解释结果:\n{explanation_result}")
