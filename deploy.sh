#! /usr/bin/env sh
echo "######START######"
echo $("date")

git pull
scrapy crawl gtja

echo "######END######"
echo "\n\n"

