def gen_list_from_text(text):
    result_list = []
    for result in text.split("- "):
        if len(result) <= 0:
            continue
        result_list.append(
            result.lower() if result[-1] != "\n" else result[:-1].lower())
    return result_list