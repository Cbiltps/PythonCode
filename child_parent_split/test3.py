def split_file(file_content: str):
    import re

    level1_pattern = re.compile(r"^##\s+(\d+)[、.]?\s*(.+)$")
    level2_pattern = re.compile(r"^###\s+(\d+\.\d+)\s+(.+)$")
    level3_pattern = re.compile(r"^####\s+(\d+\.\d+\.\d+)\s+(.+)$")

    chunks = []  # 存储所有分块结果
    current_hierarchy = {
        "level1": None,  # 当前一级标题 (编号, 标题)
        "level2": None,  # 当前二级标题
        "level3": None,  # 当前三级标题
    }
    current_content = []  # 当前块的内容收集

    lines = file_content.split("\n")
    for line in lines:
        stripped_line = line.strip()
        level = None
        num = None
        title = None

        # 判断标题行并提取信息
        if stripped_line.startswith("## "):
            match = level1_pattern.match(stripped_line)
            if match:
                level = 1
                num = match.group(1)
                title = match.group(2)
        elif stripped_line.startswith("### "):
            match = level2_pattern.match(stripped_line)
            if match:
                level = 2
                num = match.group(1)
                title = match.group(2)
        elif stripped_line.startswith("#### "):
            match = level3_pattern.match(stripped_line)
            if match:
                level = 3
                num = match.group(1)
                title = match.group(2)

        if level is not None:
            # 遇到新标题，保存当前块
            if current_content:
                # 生成块标题
                title_parts = []
                if current_hierarchy["level1"]:
                    title_parts.append(
                        f"{current_hierarchy['level1'][0]} {current_hierarchy['level1'][1]}"
                    )
                if current_hierarchy["level2"]:
                    title_parts.append(
                        f"{current_hierarchy['level2'][0]} {current_hierarchy['level2'][1]}"
                    )
                if current_hierarchy["level3"]:
                    title_parts.append(
                        f"{current_hierarchy['level3'][0]} {current_hierarchy['level3'][1]}"
                    )
                chunk_title = f"《{'-'.join(title_parts)}》"
                # 合并内容并过滤空行（保留段落间换行）
                chunk_content = "\n".join(current_content).strip()
                if chunk_content:
                    chunks.append(f"{chunk_title}{chunk_content}")
                current_content = []

            # 更新层级路径
            if level == 1:
                current_hierarchy["level1"] = (num, title)
                current_hierarchy["level2"] = None
                current_hierarchy["level3"] = None
            elif level == 2:
                current_hierarchy["level2"] = (num, title)
                current_hierarchy["level3"] = None
            elif level == 3:
                current_hierarchy["level3"] = (num, title)
        else:
            # 非标题行，处理并收集内容
            stripped_line = line.strip()
            if stripped_line or (current_content and current_content[-1] != ""):
                current_content.append(stripped_line if stripped_line else "")

    # 处理最后一个块
    if current_content:
        title_parts = []
        if current_hierarchy["level1"]:
            title_parts.append(
                f"{current_hierarchy['level1'][0]} {current_hierarchy['level1'][1]}"
            )
        if current_hierarchy["level2"]:
            title_parts.append(
                f"{current_hierarchy['level2'][0]} {current_hierarchy['level2'][1]}"
            )
        if current_hierarchy["level3"]:
            title_parts.append(
                f"{current_hierarchy['level3'][0]} {current_hierarchy['level3'][1]}"
            )
        chunk_title = f"《{'-'.join(title_parts)}》"
        chunk_content = "\n".join(current_content).strip()
        if chunk_content:
            chunks.append(f"{chunk_title}{chunk_content}")

    return chunks
