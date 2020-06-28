import pandas as pd

# 複数モデルに共通メソッドを追加するためのミックスイン
class ModelMixin:
    # データをDataFrameに変換して出力する
    # 引数：レコードIDのリスト
    @classmethod
    def values_as_dataframe_by_ids(cls, ids):
        query = cls.query.filter(cls.id.in_(ids))
        racer_dict = {}
        for row in query:
            row_dict = row.__dict__
            del row_dict["_sa_instance_state"], row_dict["created_at"]
            row_dict[cls.__tablename__ + "_id"] = row.id
            racer_dict[row.id] = row_dict
        result_df = pd.DataFrame(racer_dict).T
        return result_df.drop("id", axis=1, errors="ignore")

    @classmethod
    def values_as_dataframe_by_query(cls, query):
        racer_dict = {}
        for row in query:
            row_dict = row.__dict__
            del row_dict["_sa_instance_state"], row_dict["created_at"]
            row_dict[cls.__tablename__ + "_id"] = row.id
            racer_dict[row.id] = row_dict
        result_df = pd.DataFrame(racer_dict).T
        # query結果が0件だとidをdropするときにエラーを起こすのでignore
        return result_df.drop("id", axis=1, errors="ignore")