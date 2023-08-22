def load():
    file_db = wiz.model('orm').use('files')
    rows_2020 = file_db.rows(year='2020', fields="rows")
    count_2020 = 0
    for row in rows_2020:
        row = int(row['rows'])
        count_2020 += row

    rows_2021 = file_db.rows(year='2021', fields="rows")
    count_2021 = 0
    for row in rows_2021:
        row = int(row['rows'])
        count_2021 += row

    rows_2022 = file_db.rows(year='2022', fields="rows")
    count_2022 = 0
    for row in rows_2022:
        row = int(row['rows'])
        count_2022 += row
    
    rowName = ['2020년도', '2021년도', '2022년도']
    rowCount = [count_2020, count_2021, count_2022]

    result = dict()
    result['datas'] = rowCount
    result['labels'] = rowName

    wiz.response.status(200, result)