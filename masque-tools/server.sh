#!/bin/bash

proxy_port=${proxy_port:-1024}

./masque_server \
    --port="$proxy_port" \
    --allow_unknown_root_cert=true \
    --certificate_file=certs/certificate.pem \
    --key_file=certs/key-pkcs8.pem
