#!/bin/sh -e

rm out.txt

find ../tests/examples/gitbook/cmp-docs -type f -name '*.md' |
    while read -r file; do
        tmpfile="$(mktemp)"
        pandoc -f markdown -t plain -o "${tmpfile}" "${file}"
        # https://github.com/koalaman/shellcheck/wiki/SC2002
        # shellcheck disable=SC2002
        cat "${tmpfile}" |
            sed 's,_‌*,,g' |
            sed 's,\**,,g' |
            sed 's,\[*,,g' |
            sed 's,\]*,,g' |
            sed 's,{%.*%},,g' |
            sed 's,{%*,,g' |
            sed 's,%\}*,,g' |
            sed 's,endhint, ,g' \
                >>out.txt
    done
