#!/bin/bash

function zeroout()
{
	objcopy --dump-section "$1"=sec.bin a.out
	xxd -p sec.bin  | sed 's/[0-9a-f]/0/g' | xxd -r -p > seczero.bin
	objcopy --update-section "$1"=seczero.bin a.out
	rm -f sec.bin
	rm -f seczero.bin
}

function check_diff()
{
	diff $1 $2 > /dev/null 2>&1
	if [ $? -ne 1 ]; then
		echo "FAILED: zero binary failed"
		exit 1
	fi
}

function check_size()
{
	if [ `ls -l a.out | awk '{ print $5 }'` -gt 32000 ]; then
		echo "FAILED: binary is too big"
		exit 1
	fi
}

gcc -O code.c -m32 -o a.out -w
cp -f a.out a.out.orig

check_size

zeroout ".text"

check_diff "a.out" "a.out.orig"

rm -f a.out.orig

exit 0
