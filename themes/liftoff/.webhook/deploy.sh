#!/usr/bin/env bash

set -euo pipefail

DOCROOT="hugo-liftoff.kevinhorst.de"

echo "Deploy package liftoff-$1 on $2..."

if [[ $2 == "production" ]]; then
  staging="${DOCROOT}.new-$1"
  previous="${DOCROOT}.old-$1"

  # Unpack beside the live docroot, then swap. Extracting straight into
  # it would serve a half-written site and leave stale fingerprinted
  # assets behind, since tar overwrites but never deletes.
  rm -rf "$staging"
  mkdir -p "$staging"
  tar -xzf "${ENV_DEPLOY_PACKAGE}" -C "$staging" --strip-components=1
  chmod -R u=rwX,go=rX "$staging"

  if [[ -d $DOCROOT ]]; then
    mv "$DOCROOT" "$previous"
  fi
  mv "$staging" "$DOCROOT"
  rm -rf "$previous"
else
  echo "Unknown environment." >&2
  exit 1
fi
