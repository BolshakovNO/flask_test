#!/bin/bash
if [ ! -d rethinkdb-2.3.0 ]; then
    wget https://download.rethinkdb.com/dist/rethinkdb-2.3.0.tgz
	tar xf rethinkdb-2.3.0.tgz
    rm rethinkdb-2.3.0.tgz
    cd rethinkdb-2.3.0
	./configure --allow-fetch
	make
fi

