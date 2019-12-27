def extract(node, xpath, is_text=False):
    result = node.xpath(xpath)
    if not result:
        return '' if is_text else None
    return result[0].text_content().strip() if is_text else result[0]
