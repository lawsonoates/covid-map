from src.db import db_latest_date

def test_db_latest_date():
    date_str_1 = '2021-09-03 04:21:20'
    date_str_2 = '2021-09-04 04:21:20'

    assert db_latest_date(date_str_1, date_str_2, '%Y-%m-%d %H:%M:%S') == date_str_2

