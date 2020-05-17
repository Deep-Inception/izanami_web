from app.scraper import result_download, data_download
import pytest
import datetime

def test_get_result_download_url():
    date = datetime.date(2020, 5, 10)
    req = result_download.get_request(date)
    assert req.status_code == 200

def test_get_data_download_url():
    date = datetime.date(2020, 5, 10)
    req = data_download.get_request(date)
    assert req.status_code == 200
