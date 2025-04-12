from app.utils import paginate_list

def test_paginate_list_default():
    items = list(range(1, 21))  # 20 items
    result = paginate_list(items)
    assert result == list(range(1, 11))

def test_paginate_list_custom_page():
    items = list(range(1, 51))
    result = paginate_list(items, page_num=2, per_page=15)
    assert result == list(range(16, 31))