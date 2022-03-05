#!/bin/sh -e

OUTPUT_DIR="out"

mkdir -p "${OUTPUT_DIR}"

DOCS="${OUTPUT_DIR}/cmp-docs.html"

force_tidy() {
    tidy -wrap 0 -bare -omit -utf8 -f /dev/null -modify "${1}" || true
}

# Convert Markdown files to HTML and then convert to plain text
find ../clones/cmp-docs -type f -name '*.md' |
    while read -r file; do
        echo "Processing: ${file}"
        temp_html="$(mktemp)"
        pandoc -f markdown -t html -o "${temp_html}" "${file}"
        force_tidy "${temp_html}"
        cat >>"${DOCS}" <"${temp_html}"
    done

force_tidy "${DOCS}"
