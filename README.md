# IZANAMI APP

This is Boat Racing tip App!!!

* Libraries
Python 3.6.7

Flask 1

scikit-learn 0.22.1

numpy 1.18.1

beautifulsoup4 4.8.2

python-chromedriver-binary 81.0.4044.20.0

selenium 3.141.0

lhafile 0.2.2

pytest 5.4.2

## 起動方法

* debug

    $ python manage.py

* production

    $ python app.py production

## テーブル作成

python -m initialdatasetup.db_migrate

## レースデータ一括挿入(インポートしようとした日のレースデータが既に存在する場合エラー)

python -m initialdatasetup.init_race_data

## Test実行方法

$ cd tests

$ pytest

## dockerイメージ、コンテナのビルド(開発用)

docker-compose build #image, izanami_db コンテナのビルド

docker-compose up #再起動だけならこれだけでOK
