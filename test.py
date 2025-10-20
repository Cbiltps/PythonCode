import mimetypes

content_type, _ = mimetypes.guess_type(
    "C:\Learning\Code\PythonCode\\temp\mp.weixin.qq.com_Untitled.md"
)
print(content_type)
