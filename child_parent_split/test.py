def split_file(file_content: str):
    """
    将Markdown格式的文件内容按照两层父子级结构进行分块。
    父文档：一级标题（## 标题）及其下所有内容（包括二级、三级标题的内容）
    子文档：父文档直属内容、二级标题（### 标题）和三级标题（#### 标题）及其内容
    
    Args:
        file_content: Markdown格式的文件内容字符串
    
    Returns:
        list: 分块后的内容列表，每个元素为字典，按文档顺序：父文档 -> 直属子文档 -> 二级标题子文档 -> 三级标题子文档
              {
                  'id': int,  # 文档ID，父文档有唯一ID，子文档为None
                  'pid': int,  # 父文档ID，父文档为-1，子文档为其父文档ID
                  'sort_id': int,  # 排序ID，仅子文档有，用于全局顺序展示
                  'chunk': str  # 文档内容，格式为"《标题层级路径》内容"
              }
    """
    import re
    import time

    # 定义标题的正则匹配模式
    level1_pattern = re.compile(r"^##\s+(\d+)[、.]?\s*(.+)$")  # 匹配一级标题：## 1. 标题
    level2_pattern = re.compile(r"^###\s+(\d+\.\d+)\s+(.+)$")  # 匹配二级标题：### 1.1 标题
    level3_pattern = re.compile(r"^####\s+(\d+\.\d+\.\d+)\s+(.+)$")  # 匹配三级标题：#### 1.1.1 标题

    chunks = []  # 存储所有分块结果
    parent_id_counter = int(time.time() * 1000)  # 使用时间戳生成唯一ID
    child_sort_counter = 0  # 子文档全局排序计数器
    
    # 第一步：解析文档结构，收集每个章节的内容
    lines = file_content.split("\n")
    sections = []  # 存储每个一级标题（章节）
    current_section = None
    
    for line in lines:
        stripped_line = line.strip()
        
        # 检查是否为一级标题
        level1_match = level1_pattern.match(stripped_line)
        if level1_match:
            if current_section is not None:
                sections.append(current_section)
            
            num = level1_match.group(1)
            title = level1_match.group(2)
            parent_id_counter += 1
            current_section = {
                'num': num,
                'title': title,
                'parent_id': parent_id_counter,
                'all_lines': [],  # 所有内容行（用于父文档）
                'direct_lines': [],  # 直属内容行（用于直属子文档）
                'subsections': []  # 二级、三级标题
            }
            continue
        
        if current_section is not None:
            # 收集所有内容
            stripped_content = line.strip()
            if stripped_content or (current_section['all_lines'] and current_section['all_lines'][-1] != ""):
                current_section['all_lines'].append(stripped_content if stripped_content else "")
    
    # 保存最后一个章节
    if current_section is not None:
        sections.append(current_section)
    
    # 第二步：处理每个章节，解析二级、三级标题
    for section in sections:
        subsections = []
        current_subsection = None
        current_level2 = None  # 记录当前二级标题
        
        in_subsection = False  # 标记是否已经进入子标题区域
        
        for line in section['all_lines']:
            # 检查是否为二级标题
            level2_match = level2_pattern.match(line)
            if level2_match:
                if current_subsection is not None:
                    subsections.append(current_subsection)
                
                num = level2_match.group(1)
                title = level2_match.group(2)
                current_subsection = {
                    'num': num,
                    'title': title,
                    'level': 2,
                    'lines': [],
                    'parent_level2': None
                }
                current_level2 = (num, title)
                in_subsection = True
                continue
            
            # 检查是否为三级标题
            level3_match = level3_pattern.match(line)
            if level3_match:
                if current_subsection is not None:
                    subsections.append(current_subsection)
                
                num = level3_match.group(1)
                title = level3_match.group(2)
                current_subsection = {
                    'num': num,
                    'title': title,
                    'level': 3,
                    'lines': [],
                    'parent_level2': current_level2
                }
                in_subsection = True
                continue
            
            # 内容行
            if current_subsection is not None:
                # 子标题下的内容
                if line or (current_subsection['lines'] and current_subsection['lines'][-1] != ""):
                    current_subsection['lines'].append(line if line else "")
            elif not in_subsection:
                # 直属内容（还没遇到任何子标题）
                if line or (section['direct_lines'] and section['direct_lines'][-1] != ""):
                    section['direct_lines'].append(line if line else "")
        
        # 保存最后一个子标题
        if current_subsection is not None:
            subsections.append(current_subsection)
        
        section['subsections'] = subsections
    
    # 第三步：按顺序生成chunks
    for section in sections:
        # 1. 保存父文档
        chunk_title = f"《{section['num']} {section['title']}》"
        chunk_content = "\n".join(section['all_lines']).strip()
        if chunk_content:
            chunks.append({
                'id': section['parent_id'],
                'pid': -1,
                'sort_id': None,
                'chunk': f"{chunk_title}{chunk_content}"
            })
        
        # 2. 保存父文档的直属内容作为子文档（如果有）
        direct_content = "\n".join(section['direct_lines']).strip()
        if direct_content:
            child_sort_counter += 1
            chunks.append({
                'id': None,
                'pid': section['parent_id'],
                'sort_id': child_sort_counter,
                'chunk': f"{chunk_title}{direct_content}"
            })
        
        # 3. 保存所有子标题
        for subsection in section['subsections']:
            # 构建子标题路径
            if subsection['level'] == 2:
                sub_title = f"《{section['num']} {section['title']}-{subsection['num']} {subsection['title']}》"
            else:  # level == 3
                if subsection['parent_level2'] is not None:
                    parent_num, parent_title = subsection['parent_level2']
                    sub_title = f"《{section['num']} {section['title']}-{parent_num} {parent_title}-{subsection['num']} {subsection['title']}》"
                else:
                    sub_title = f"《{section['num']} {section['title']}-{subsection['num']} {subsection['title']}》"
            
            sub_content = "\n".join(subsection['lines']).strip()
            if sub_content:
                child_sort_counter += 1
                chunks.append({
                    'id': None,
                    'pid': section['parent_id'],
                    'sort_id': child_sort_counter,
                    'chunk': f"{sub_title}{sub_content}"
                })
    
    return chunks
