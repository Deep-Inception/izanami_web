import pytest
import pandas as pd
from backend.views import prediction

def test_raw_data_001():
    data = merged_data_for_test_001()
    result = prediction.raw_data(data)
    assert len(result) == 2;

def merged_data_for_test_001():
    return pd.DataFrame(data=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, None, 7], [1, 2, 3, 4, 5, 6, 7]],
                        columns=["time", "place", "deadline", "distance", "couse", "racer_id", "exhibition_time"])

# timeがNoneでも削除しない
def test_raw_data_002():
    data = merged_data_for_test_002()
    result = prediction.raw_data(data)
    assert len(result) == 3;

def merged_data_for_test_002():
    return pd.DataFrame(data=[[1, 2, 3, 4, 5, 6, 7], [None, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7]],
                        columns=["time", "place", "deadline", "distance", "couse", "racer_id", "exhibition_time"])

# timeがNoneかつ他もNoneなら削除する
def test_raw_data_003():
    data = merged_data_for_test_003()
    result = prediction.raw_data(data)
    assert len(result) == 2;

def merged_data_for_test_003():
    return pd.DataFrame(data=[[1, 2, 3, 4, 5, 6, 7], [None, 2, 3, 4, 5, None, 7], [1, 2, 3, 4, 5, 6, 7]],
                        columns=["time", "place", "deadline", "distance", "couse", "racer_id", "exhibition_time"])

def test_merge_train_data():
    race_data = race_data_for_test()
    racer_data = racer_data_for_test()
    result_data = race_result_data_for_test()
    result = prediction.merge_train_data(race_data, racer_data, result_data)
    assert len(result) == 3
    assert result["race_id"][0] == 1
    assert result["race_id"][1] == 1
    assert result["race_id"][2] == 2
    assert result["prize"][0] == 1
    assert result["prize"][1] == 2

def race_data_for_test():
    return pd.DataFrame(data=[[1], [2]], columns=["race_id"])

def racer_data_for_test():
    return pd.DataFrame(data=[[1, 1],[1, 2], [2, 3]], columns=["race_id", "timetable_racer_id"])

def race_result_data_for_test():
    return pd.DataFrame(data=[[1, 1],[2, 2], [3, 1]], columns=["timetable_racer_id", "prize"])