#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

registry='quay.io'
organization='innovation-hub-bergisches-rheinland'
repository='showcase-3d-printer-anomaly-counter'
tag='local'
builder='gcr.io/buildpacks/builder'
builder_version='v1'

workdir="$(
    cd "$(dirname "$0")"
    pwd
)"

poetry export -f 'requirements.txt' >"${workdir}/requirements.txt"

pack build "${registry}/${organization}/${repository}:${tag}" \
    --builder="${builder}:${builder_version}" \
    --path="${workdir}" \
    --descriptor="${workdir}/project.toml"

rm --force "${workdir}/requirements.txt"
