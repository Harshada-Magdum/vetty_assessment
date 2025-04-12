def paginate_list(data, page_num=1, per_page=10):
    start = (page_num - 1) * per_page
    end = start + per_page
    return data[start:end]
