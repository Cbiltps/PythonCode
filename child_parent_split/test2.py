def split_file(file_content: str):
    """
    将包含章节、条款和附件的文本内容按照父子级结构进行分块处理。
    父文档：每个章节（第X章）及其所有内容
    子文档：每个条款（第X条）
    适用于法律文件、政策文件等结构化文本的拆分。
    
    Args:
        file_content: 待处理的文本内容字符串
    
    Returns:
        list: 分块后的内容列表，每个元素为字典：
              {
                  'id': int,  # 文档ID，父文档（章节）有唯一ID，子文档（条款）为None
                  'pid': int,  # 父文档ID，父文档为-1，子文档为其所属章节的ID
                  'sort_id': int,  # 排序ID，仅子文档有，用于全局顺序展示
                  'chunk': str  # 文档内容，格式为"《标题》内容"
              }
    """
    import re
    import time
    
    # 1. 分离正文和附件部分
    # 查找附件起始位置（"附件："或"附件:"）
    catalogue_match = re.search(r'附件[：:]', file_content)
    if catalogue_match:
        # 找到附件标记，分离正文和附件
        main_text = file_content[:catalogue_match.start()]  # 正文部分
        attachments_text = file_content[catalogue_match.start():]  # 附件部分（包含"附件"标记）
    else:
        # 未找到附件标记，全部视为正文
        main_text = file_content
        attachments_text = ''

    # 2. 正文分块（父文档：章节，子文档：条款）
    # 定义章节模式：匹配"第X章 章节标题"
    chapter_pattern = r'(第[一二三四五六七八九十]+章 [^\n]+)'
    chapter_iter = list(re.finditer(chapter_pattern, main_text))  # 查找所有章节
    
    # 定义条款模式：匹配"第X条"
    article_pattern = r'(第[一二三四五六七八九十]+条)'
    article_iter = list(re.finditer(article_pattern, main_text))  # 查找所有条款

    blocks = []  # 存储所有分块结果
    parent_id_counter = int(time.time() * 1000)  # 使用时间戳生成唯一ID
    child_sort_counter = 0  # 子文档全局排序计数器
    
    # 为每个章节创建父文档，并为其下的条款创建子文档
    for chap_idx, chap in enumerate(chapter_iter):
        chap_start = chap.start()  # 章节起始位置
        chap_name = chap.group(1)  # 章节名称
        parent_id_counter += 1
        current_parent_id = parent_id_counter  # 当前章节的ID
        
        # 确定章节内容范围（到下一章节或正文结束）
        chap_end = chapter_iter[chap_idx+1].start() if chap_idx+1 < len(chapter_iter) else len(main_text)
        chapter_content = main_text[chap.end():chap_end].strip()  # 章节下的所有内容
        
        # 添加父文档（章节）
        blocks.append({
            'id': current_parent_id,  # 父文档有唯一ID
            'pid': -1,  # 父文档pid为-1
            'sort_id': None,  # 父文档没有sort_id
            'chunk': f"《{chap_name}》{chapter_content}"
        })
        
        # 查找该章节下的所有条款
        for art in article_iter:
            art_start = art.start()
            # 条款在当前章节范围内
            if chap_start < art_start < chap_end:
                art_end = art.end()  # 条款结束位置
                
                # 确定条款内容范围（到下一条款或章节结束）
                # 查找该章节内的下一个条款
                next_art_start = chap_end
                for next_art in article_iter:
                    if next_art.start() > art_start and next_art.start() < chap_end:
                        next_art_start = next_art.start()
                        break
                
                article_content = main_text[art_end:next_art_start].strip()  # 提取条款内容
                
                # 添加子文档（条款）
                child_sort_counter += 1
                blocks.append({
                    'id': None,  # 子文档没有id
                    'pid': current_parent_id,  # 关联到父文档（章节）
                    'sort_id': child_sort_counter,  # 全局排序ID
                    'chunk': f"《{chap_name} - {art.group(1)}》{article_content}"
                })

    # 3. 附件分块（父文档：附件整体，子文档：每个附件）
    if attachments_text:  # 如果存在附件部分
        # 创建附件父文档
        parent_id_counter += 1
        attachments_parent_id = parent_id_counter
        
        # 附件父文档包含所有附件内容
        blocks.append({
            'id': attachments_parent_id,  # 附件父文档有唯一ID
            'pid': -1,  # 附件父文档pid为-1
            'sort_id': None,  # 附件父文档没有sort_id
            'chunk': f"《附件》{attachments_text.strip()}"
        })
        
        # 定义附件模式：匹配"附件 1"、"附件1:"等格式
        attachment_pattern = r'(附件\s*\d+\s*[：:]?)'
        attachment_iter = list(re.finditer(attachment_pattern, attachments_text))  # 查找所有附件标记

        # 遍历每个附件，提取内容作为子文档
        for idx, att in enumerate(attachment_iter):
            att_start = att.end()  # 附件标题结束位置
            att_title_raw = att.group(0)  # 原始附件标题（可能包含冒号和空格）
            att_title = re.sub(r'\s*[：:]\s*$', '', att_title_raw)  # 去掉结尾的冒号及空格，规范化标题
            
            # 确定当前附件的内容范围（到下一附件或附件部分结束）
            next_start = attachment_iter[idx+1].start() if idx+1 < len(attachment_iter) else len(attachments_text)
            content = attachments_text[att_start:next_start].strip()  # 提取附件内容
            
            # 每个附件作为子文档，关联到附件父文档
            child_sort_counter += 1
            blocks.append({
                'id': None,  # 子文档没有id
                'pid': attachments_parent_id,  # 关联到附件父文档
                'sort_id': child_sort_counter,  # 全局排序ID
                'chunk': f"《{att_title}》{content}"
            })
    
    return blocks
