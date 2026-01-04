#!/usr/bin/env bash

##test api token valididty


read -p "Token: " token
##Open AI search query to use:

curl -X GET "https://api.openai.com/v1/models" -H "Authorization: Bearer $token " -H "Accept: application/json" -A "Mozilla/5.0 (Linux; Android 12; BTK-W09 Build/HUAWEIBTK-W09; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.196 Safari/537.36 HuaweiBrowser/16.0.6.300 HMSCore/6.15.4.322"  -v




