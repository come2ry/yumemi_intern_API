# Yumemi Intern 検閲API
> 機密保持のためプロジェクト固有の単語が含まれていないかを確認できる検閲用のAPI

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/tkrk1209/yumemi_intern_API)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/tkrk1209/yumemi_intern_API/fastapi)
![GitHub MySQL version](https://img.shields.io/badge/mysql-5.7-green)


![](header.png)

## Pre Installation
OS X:

```sh
brew install pyenv
brew install pipenv
```
1. MAMPをダウンロードしてMySQLのポートを3306に指定
2. yumemi_dbを作成
3. .envを作成し、以下の[]を任意の文字に置き換える
```sh
GAE_ENV=
DEBUG_MODE=true
PROJECT_NAME=[任意のプロジェクト名]

SERVER_NAME=
API_LOCATION=http://127.0.0.1:8000

MYSQL_SERVER=127.0.0.1:3306
MYSQL_USER=[MySQLユーザ名]
MYSQL_PASSWORD=[MySQLパスワード]
MYSQL_DATABASE=[DB名]
```

## Installation

```sh
pipenv install
make init
```

## Usage example

```sh
make run
```

http://127.0.0.1:8000/docs
へアクセスするとSwaggerが起動

## Development setup

追記中

## Release History

追記中

<!-- Markdown link & img dfn's -->
