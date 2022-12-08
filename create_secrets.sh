#!/bin/bash

export $(cat .env | xargs)
secrets_dir="kubernetes/secrets"
secrets=$(ls ${secrets_dir})

for secret in ${secrets[@]}
do
    envsubst < ${secrets_dir}/$secret > tmp_secret
    mv tmp_secret ${secrets_dir}/$secret
done
