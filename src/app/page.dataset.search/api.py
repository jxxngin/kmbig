import math
import re
import json

def load():
    page = wiz.request.query("page", 1)
    search_word = wiz.request.query("text", "")
    mode = wiz.request.query("mode", True)
    data = wiz.request.query()

    checked = wiz.request.query("checked", "{}")
    checked = json.loads(checked)

    checked_result = {}

    for key in checked:
        true_keys = []
        for inner_key, value in checked[key].items():
            if value:
                true_keys.append(inner_key)
        if true_keys:
            checked_result[key] = true_keys

    def get_values(checked_result, key):
        if key in checked_result and checked_result[key]:
            return checked_result[key]
        return None

    page = int(page)
    db = wiz.model('orm').use('dataset')

    if mode == "default":
        orderby = 'title'
        order = 'ASC'
    elif mode == "update":
        orderby = 'update'
        order = 'DESC'
    elif mode == "view":
        orderby = 'view_count'
        order = 'DESC'
    elif mode == "download":
        orderby = 'download_count'
        order = 'DESC'

    where = {
        'title': search_word,
    }
    like = 'title'
    
    for field in ['category', 'department', 'filetype', 'visibility']:
        values = get_values(checked_result, field)
        if values is not None:
            where[field] = values
    
    total = db.count(like=like, **where)
    rows = db.rows(
        page=page,
        orderby=orderby,
        order=order,
        like=like,
        fields="id,title,category,summary,filetype,tags,visibility,identification,department,view_count,download_count,created,updated",
        **where
    )
    cnt = db.count(page=page, like=like, **where)
    lastpage = math.ceil(cnt / 10)

    def filtered(where, excluded_key):
        return {key: value for key, value in where.items() if key != excluded_key}
    
    keys = ['department', 'category', 'filetype', 'visibility']
    facet_results = dict()

    for key in keys:
        filtered_where = filtered(where, key)
        facet_results[key] = db.facet_rows(facet=key, groupby=key, order='DESC', orderby=key, like=like, **filtered_where)
    
    # dpt_rows = db.facet_rows(facet='department', groupby='department', order='DESC', orderby='department', like=like, **(filtered(where, "department")))
    # ctgy_rows = db.facet_rows(facet='category', groupby='category', order='DESC', orderby='category', like=like, **(filtered(where, "category")))
    # ft_rows = db.facet_rows(facet='filetype', groupby='filetype', order='DESC', orderby='filetype', like=like, **(filtered(where, "filetype")))
    # vsb_rows = db.facet_rows(facet='visibility', groupby='visibility', order='DESC', orderby='visibility', like=like, **(filtered(where, "visibility")))

    def sort_cnt(item):
        return (-item['cnt'], item['name'])

    facet = dict()
    for key in keys:
        facet[key] = sorted(facet_results[key], key=sort_cnt)
    # facet['department'] = sorted(dpt_rows, key=sort_cnt)
    # facet['category'] = sorted(ctgy_rows, key=sort_cnt)
    # facet['filetype'] = sorted(ft_rows, key=sort_cnt)
    # facet['visibility'] = sorted(vsb_rows, key=sort_cnt)

    wiz.response.status(200, {
        "list": rows,
        "lastpage":lastpage,
        "total": total,
        "facet": facet,
    })