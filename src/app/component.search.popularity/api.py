from collections import Counter

def load():
    rows = wiz.model('orm').use('log_search').rows(fields="search_text")
    res = list(map(lambda x: x['search_text'], rows))

    counter = Counter(res)

    result = []
    for title, cnt in counter.items():
        result.append({"title": title, "cnt": cnt})
    result = sorted(result, key=lambda x: x['cnt'], reverse=True)

    top_5 = result[:5]
    data = []
    for item in top_5:
        data.append(item['title'])

    wiz.response.status(200, data)

def log():
    text = wiz.request.query("text", True)
    wiz.model('orm').use('log_search').search_log(text)

    wiz.response.status(200)