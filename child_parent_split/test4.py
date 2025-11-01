
def split_file(file_content:str):
    import re
    # 1. 找到真正的附件目录起点（“附件：”或“附件:”）
    catalogue_match = re.search(r'附件[：:]', file_content)
    if catalogue_match:
        main_text = file_content[:catalogue_match.start()]
        attachments_text = file_content[catalogue_match.start():]
    else:
        main_text = file_content
        attachments_text = ''

        # 2. 正文分块
    chapter_pattern = r'(第[一二三四五六七八九十]+章 [^\n]+)'
    chapter_iter = list(re.finditer(chapter_pattern, main_text))
    article_pattern = r'(第[一二三四五六七八九十]+条)'
    article_iter = list(re.finditer(article_pattern, main_text))

    blocks = []
    for idx, art in enumerate(article_iter):
        art_start = art.start()
        art_end = art.end()
        next_start = article_iter[idx+1].start() if idx+1 < len(article_iter) else len(main_text)
        content = main_text[art_end:next_start].strip()
        # 查找所属章节
        chapter_name = ''
        for chap in reversed(chapter_iter):
            if chap.start() < art_start:
                chapter_name = chap.group(1)
                break
        if chapter_name:
            block_title = f'《{chapter_name} - {art.group(1)}》'
        else:
            block_title = f'《{art.group(1)}》'
            # blocks.append(f'{block_title}{content}')

        blocks.append(f"{block_title}{content}")

    # 3. 附件分块（只在附件部分操作）
    attachment_pattern = r'(附件\s*\d+\s*[：:]?)'
    attachment_iter = list(re.finditer(attachment_pattern, attachments_text))

    for idx, att in enumerate(attachment_iter):
        att_start = att.end()
        att_title_raw = att.group(0)
        att_title = re.sub(r'\s*[：:]\s*$', '', att_title_raw)  # 去掉结尾的冒号及空格
        next_start = attachment_iter[idx+1].start() if idx+1 < len(attachment_iter) else len(attachments_text)
        content = attachments_text[att_start:next_start].strip()
        # blocks.append(f'《{att_title}》{content}')
        blocks.append(f"《{att_title}》{content}")
    return blocks
