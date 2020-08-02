import pandas as pd
from backend import preprocessing_racer_pred_dl

def test_fill_null_time_001():
    pp = preprocessing_racer_pred_dl.RacerPredDlPreprocessor()
    pp.y = pd.DataFrame(data=[[1], [None], [None], [7]], columns=["RACE_TIME"])
    pp.fill_null_time()
    pp.y[0] = 1
    pp.y[1] = 2
    pp.y[2] = 3
    pp.y[3] = 7
    assert len(pp.y) == 4;

def merged_data_for_test():
    return pd.DataFrame(data=[[1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, None, 7], [1, 2, 3, 4, 5, 6, 7]],
                        columns=["time", "place", "deadline", "distance", "couse", "racer_id", "exhibition_time"])

def race_data_for_test():
    return pd.DataFrame(data=[[1], [2]], columns=["race_id"])

def racer_data_for_test():
    return pd.DataFrame(data=[[1, 1],[1, 2], [2, 3]], columns=["race_id", "timetable_racer_id"])

def race_result_data_for_test():
    return pd.DataFrame(data=[[1, 1],[2, 2], [3, 1]], columns=["timetable_racer_id", "prize"])