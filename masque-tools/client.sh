#!/bin/bash

proxy_addr=${proxy_addr:-localhost:1024}
website=${website:-www.google.com}

./masque_client \
    --allow_unknown_root_cert=true \
    --disable_certificate_verification=true \
    "$proxy_addr"\
    https://"$website"
