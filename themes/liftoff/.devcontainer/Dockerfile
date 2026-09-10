FROM mcr.microsoft.com/devcontainers/base:trixie

ARG HUGO_VERSION
ARG TARGETARCH

RUN curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${TARGETARCH}.tar.gz" \
    | tar -xz -C /usr/local/bin hugo \
 && hugo version
