# IZANAMI APP

This is Boat Racing tip App!!!

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

## mysql

### izanamiユーザを作る

docker exec -i -t izanami-mysql bash

mysql -u root -p 

password

use mysql

CREATE USER izanami@'localhost' IDENTIFIED BY 'izanami';

grant all on db_izanami.* to izanami@localhost;

### データベースを作る

docker exec -i -t izanami-backend bash

python -m initialdatasetup.db_migrate (テーブル作成)

mysql -u izanami -pizanami db_izanami < dump.sql
