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

    $ python app.py

* production

    $ python app.py production

## Test実行方法

$ cd tests

$ pytest

## docker環境構築手順

### dockerイメージ、コンテナのビルド

docker image build -t izanami-dev -f Dockerfile.dev . #flaskに新しいライブラリを入れた場合はこの実行が必要

docker-compose build #mysql image, izanami_db コンテナのビルド

docker-compose up #再起動だけならこれだけでOK

### db再構築

python -m config.db_migrate

### veu dev 立ち上げ

docker exec -it izanami-dev npm run dev --prefix /frontend

