#!/bin/sh -e

# POSIX locale
LC_ALL=C
export LC_ALL

# ANSI formatting
BOLD=[1m
RESET=[0m

BUILD_DIR=$(dirname "${0}")
RULES="${BUILD_DIR}/rules.mk"

get_targets() {
    file="${1}"
    grep -E '^.PHONY:' "${file}" |
        sed -E "s,^.PHONY: ,,"
}

format_targets() {
    basename="${1}"
    command="make -f ${BUILD_DIR}/${basename} \x1b${BOLD}\1\x1b${RESET}"
    sed -E "s,(.*),  ${command}," </dev/stdin

}

check_sort() {
    file="${1}"
    tmp_orig="$(mktemp)"
    get_targets "${file}" >"${tmp_orig}"
    tmp_sorted="$(mktemp)"
    get_targets "${file}" | sort >"${tmp_sorted}"
    # Color targets to indicate whether they are ordered incorrectly in the
    # source file
    diff --color=always -u \
        --label "${file}" "${tmp_orig}" \
        --label "${file}.sorted" "${tmp_sorted}"
}

print_targets() {
    file="${1}"
    basename="$(basename "${file}")"
    stem="$(echo "${basename}" | cut -f 1 -d '.')"
    echo "Available ${stem}:"
    echo
    get_targets "${file}" | sort |
        format_targets "${basename}"
}

if test "${1}" = "--check"; then
    check_sort "${RULES}"
else
    print_targets "${RULES}"
fi
