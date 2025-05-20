#!/bin/bash
# wait-for-it.sh

set -e

host="$1"
shift
cmd="$@"

until nc -z -v -w30 "$host" "${host#*:}"
do
  echo "Waiting for $host to be ready..."
  sleep 2
done

echo "$host is ready!"
exec $cmd 