"""
使用 LangChain 的 ChatTongyi 连接通义千问 qwen3-32b 模型
"""

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage

# ============ 配置区域 ============
# 请在这里填入你的通义千问 API Key (DashScope API Key)
DASHSCOPE_API_KEY = "sk-7bbd0bbbddf9480aab0769df97b183ca"

# 模型名称
MODEL_NAME = "qwen3-32b"  # qwen-plus 对应 32B 参数的模型


def main():
    """主函数 - 测试连接通义千问"""
    print("=" * 50)
    print("通义千问 qwen3-32b 连接测试")
    print("=" * 50)

    try:
        # 初始化 ChatTongyi,关闭思考模式
        chat_model = ChatTongyi(
            dashscope_api_key=DASHSCOPE_API_KEY,
            model_name=MODEL_NAME,
            temperature=0.7,
            model_kwargs={
                "enable_thinking": False,  # 关闭思考模式
            },
        )

        # 发送测试消息
        user_query = "你好"
        print(f"\n用户提问: {user_query}")
        print("-" * 50)

        # 调用模型
        response = chat_model.invoke([HumanMessage(content=user_query)])

        print(f"模型回复: {response.content}")
        print("=" * 50)
        print("测试成功!")

    except Exception as e:
        print(f"\n错误: {str(e)}")
        print("\n请检查:")
        print("1. API Key 是否正确配置 (第 9 行)")
        print("2. 是否安装了依赖: pip install langchain-community langchain-core")
        print("3. 网络连接是否正常")
        print("4. API Key 是否有效且有足够额度")


if __name__ == "__main__":
    main()
