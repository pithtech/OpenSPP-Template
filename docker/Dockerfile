# syntax=docker/dockerfile:1
# OpenSPP Training Template - Docker image
#
# Odoo 19.0 (OCA/OCB) + OpenSPP v2 (pinned release) + OCA dependencies.
# Participant modules (dswd_*) are NOT baked in: they are volume-mounted at
# /mnt/extra-addons/custom by docker-compose.yml so the container always runs
# the code on disk.
#
# The OpenSPP release is pinned once, in ../.env (OPENSPP_REF); docker compose
# passes it as a build arg. Bump that value and rebuild to move to a newer release.
#
# Build (via compose, preferred):  docker compose build odoo-app
# Build (direct):                  docker build --target dev --build-arg OPENSPP_REF=2026.09 -f docker/Dockerfile -t openspp-template-dev .

ARG PYTHON_VERSION=3.13

# =============================================================================
# Stage 1: Builder - Install all Python packages with build dependencies
# =============================================================================
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

ARG ODOO_SOURCE=OCA/OCB
ARG ODOO_VERSION=19.0

# Install ALL build dependencies once
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libcairo2-dev \
        libffi-dev \
        libfreetype6-dev \
        libfribidi-dev \
        libgeos-dev \
        libghc-zlib-dev \
        libharfbuzz-dev \
        libjpeg-dev \
        liblcms2-dev \
        libldap2-dev \
        libopenjp2-7-dev \
        libpq-dev \
        libproj-dev \
        libsasl2-dev \
        libssl-dev \
        libtiff5-dev \
        libwebp-dev \
        libxml2-dev \
        libxslt-dev \
        tcl-dev \
        tk-dev \
        zlib1g-dev

# Create virtual environment for cleaner copying
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install uv for fast dependency management (standalone installer is faster than pip)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /opt/venv/bin/

# -----------------------------------------------------------------------------
# OpenSPP release. Declared here, after the apt layer, so bumping the release
# only invalidates the layers below.
# -----------------------------------------------------------------------------
ARG OPENSPP_REF=2026.09

# Download the OpenSPP release tarball (cached between builds) and unpack it to
# the location it will have in the runtime image. Its requirements files are
# installed from here, so the Python environment always matches the release.
RUN --mount=type=cache,target=/tmp/downloads,sharing=locked \
    set -eux; \
    OPENSPP_TARBALL="/tmp/downloads/openspp-${OPENSPP_REF}.tar.gz"; \
    if [ ! -f "$OPENSPP_TARBALL" ] || ! gzip -t "$OPENSPP_TARBALL" 2>/dev/null; then \
        rm -f "$OPENSPP_TARBALL"; \
        curl -fsSL -o "$OPENSPP_TARBALL" \
            "https://github.com/OpenSPP/OpenSPP2/archive/refs/tags/${OPENSPP_REF}.tar.gz"; \
    fi; \
    mkdir -p /opt/extra-addons/openspp; \
    tar -xzf "$OPENSPP_TARBALL" -C /opt/extra-addons/openspp --strip-components=1; \
    echo "${OPENSPP_REF}" > /opt/extra-addons/openspp/.openspp-ref

# Stage the project requirements files (dswd_* manifest deps and local overrides)
COPY requirements.txt /tmp/project-requirements.txt
COPY docker/requirements.txt /tmp/project-docker-requirements.txt

# Install everything in one resolution:
#   Odoo 19 requirements -> OpenSPP release requirements -> project requirements.
# --override files win over any other pin, project overrides last.
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    --mount=type=cache,target=/tmp/downloads,sharing=locked \
    set -eux; \
    ODOO_REQS="/tmp/downloads/odoo-${ODOO_VERSION}-requirements.txt"; \
    if [ ! -s "$ODOO_REQS" ]; then \
        rm -f "$ODOO_REQS"; \
        curl -fsSL -o "$ODOO_REQS" \
            "https://raw.githubusercontent.com/${ODOO_SOURCE}/${ODOO_VERSION}/requirements.txt"; \
    fi; \
    uv pip install \
    --override /opt/extra-addons/openspp/docker/requirements.txt \
    --override /tmp/project-docker-requirements.txt \
    -r "$ODOO_REQS" \
    -r /opt/extra-addons/openspp/requirements.txt \
    -r /opt/extra-addons/openspp/docker/requirements.txt \
    -r /tmp/project-requirements.txt \
    -r /tmp/project-docker-requirements.txt

# Download and install Odoo (cache the tarball to avoid re-downloading)
# --no-deps: Odoo's runtime dependencies are already installed above from its
# requirements.txt, which carries the correct per-Python-version pins. Odoo's
# setup.py additionally declares an unpinned PyPDF2; resolving it installs
# legacy PyPDF2 3.x, which odoo.tools.pdf then selects over pypdf and which
# crashes multi-record PDF printing (OpenSPP OP#1168).
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    --mount=type=cache,target=/tmp/downloads,sharing=locked \
    set -eux; \
    ODOO_TARBALL="/tmp/downloads/odoo-${ODOO_VERSION}.tar.gz"; \
    if [ ! -f "$ODOO_TARBALL" ] || ! gzip -t "$ODOO_TARBALL" 2>/dev/null; then \
        rm -f "$ODOO_TARBALL"; \
        curl -fsSL -o "$ODOO_TARBALL" \
            "https://github.com/${ODOO_SOURCE}/archive/refs/heads/${ODOO_VERSION}.tar.gz"; \
    fi; \
    mkdir -p /opt/odoo; \
    tar -xzf "$ODOO_TARBALL" -C /opt/odoo --strip-components=1; \
    mv /opt/odoo /opt/odoo-src; \
    mkdir -p /opt/odoo; \
    mv /opt/odoo-src /opt/odoo/odoo; \
    uv pip install --no-deps -e /opt/odoo/odoo

# Third-party addon refs. Each takes a branch or a commit sha, so a deployment
# can pin an exact commit instead of tracking a moving branch. A tag name is not
# accepted (it resolves under refs/tags, which this does not build) - pass the
# commit sha the tag points at:
# docker build --build-arg OCA_SERVER_UX_REF=<sha> ...
ARG OCA_SERVER_UX_REF=19.0
ARG OCA_SERVER_TOOLS_REF=19.0
ARG ODOO_JOB_WORKER_REF=19.0
ARG OCA_SERVER_BACKEND_REF=19.0
ARG OCA_REST_FRAMEWORK_REF=19.0
ARG MUK_IT_REF=19.0

# Download OCA and OpenSPP dependencies in builder (cache tarballs to avoid re-downloading)
RUN --mount=type=cache,target=/tmp/downloads,sharing=locked \
    set -eux; \
    download_module() { \
        local repo=$1; \
        local dest=$2; \
        local ref=${3:-19.0}; \
        local tarball="/tmp/downloads/${dest}-${ref}.tar.gz"; \
        local url="https://github.com/${repo}/archive/refs/heads/${ref}.tar.gz"; \
        # A commit sha sits under no ref namespace: GitHub serves it from
        # /archive/<sha>.tar.gz and 404s on /archive/refs/heads/<sha>.tar.gz.
        # 7+ hex digits is a sha (short or full); anything else is a branch.
        case "$ref" in \
            *[!0-9a-fA-F]*) ;; \
            ???????*) url="https://github.com/${repo}/archive/${ref}.tar.gz";; \
        esac; \
        if [ ! -f "$tarball" ] || ! gzip -t "$tarball" 2>/dev/null; then \
            rm -f "$tarball"; \
            # -f so a bad ref fails here with the 404, not later in tar with
            # "not in gzip format" over a 14-byte error body.
            curl -fsSL -o "$tarball" "$url"; \
        fi; \
        mkdir -p /opt/extra-addons/${dest}; \
        tar -xzf "$tarball" -C /opt/extra-addons/${dest} --strip-components=1; \
    }; \
    download_module "OCA/server-ux" "server-ux" "${OCA_SERVER_UX_REF}"; \
    download_module "OCA/server-tools" "server-tools" "${OCA_SERVER_TOOLS_REF}"; \
    download_module "OpenSPP/odoo-job-worker" "odoo-job-worker" "${ODOO_JOB_WORKER_REF}"; \
    download_module "OCA/server-backend" "server-backend" "${OCA_SERVER_BACKEND_REF}"; \
    download_module "OCA/rest-framework" "rest-framework" "${OCA_REST_FRAMEWORK_REF}"; \
    download_module "muk-it/odoo-modules" "muk-it" "${MUK_IT_REF}"

# Precompile Python files (ignore errors from Python 2 syntax in some packages)
RUN python -m compileall -q /opt/venv/lib/ || true

# =============================================================================
# Stage 2: Runtime - Minimal image with only runtime dependencies
# =============================================================================
FROM python:${PYTHON_VERSION}-slim-bookworm AS runtime

ARG TARGETARCH
ARG WKHTMLTOPDF_VERSION=0.12.6.1
ARG WKHTMLTOPDF_AMD64_CHECKSUM='98ba0d157b50d36f23bd0dedf4c0aa28c7b0c50fcdcdc54aa5b6bbba81a3941d'
ARG WKHTMLTOPDF_ARM64_CHECKSUM='b6606157b27c13e044d0abbe670301f88de4e1782afca4f9c06a5817f3e03a9c'
ARG GEOIP_UPDATER_VERSION=7.1.1
ARG GEOIP_AMD64_CHECKSUM='c4c964b0fabbeac4087636f4fc822a9f8c35204641675d242781a270f739b3e3'
ARG GEOIP_ARM64_CHECKSUM='687e373348973fd9a9da7e7d8f23b7cac34ad786ea7db71f280c4953f532043c'
ARG ODOO_VERSION=19.0
ARG OPENSPP_REF=2026.09
ARG UID=1000
ARG GID=1000
ARG PG_VERSION=18

LABEL org.opencontainers.image.source="https://github.com/pithtech/OpenSPP-Template" \
      org.opencontainers.image.description="Odoo 19 + OpenSPP ${OPENSPP_REF} for the DSWD 4Ps developer training" \
      org.opencontainers.image.version="${OPENSPP_REF}" \
      org.opencontainers.image.licenses="LGPL-3.0"

EXPOSE 8069 8072

# Environment variables
ENV ODOO_VERSION="${ODOO_VERSION}" \
    OPENSPP_REF="${OPENSPP_REF}" \
    ODOO_RC=/etc/odoo/odoo.conf \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PATH="/opt/venv/bin:/home/odoo/.local/bin:$PATH" \
    VIRTUAL_ENV=/opt/venv \
    PYTHONUNBUFFERED=1 \
    DB_FILTER=.* \
    LIST_DB=false \
    UNACCENT=true \
    PROXY_MODE=true \
    WITHOUT_DEMO=all

# Install runtime dependencies only (no build tools!)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        # System utilities
        curl \
        ca-certificates \
        gnupg2 \
        gettext-base \
        # Fonts for PDF generation (including wkhtmltopdf dependencies)
        fontconfig \
        fonts-liberation2 \
        fonts-dejavu-core \
        fonts-freefont-ttf \
        xfonts-75dpi \
        xfonts-base \
        # Runtime libraries (no -dev packages!)
        libcairo2 \
        libfreetype6 \
        libfribidi0 \
        libgeos-c1v5 \
        libjpeg62-turbo \
        liblcms2-2 \
        libldap-2.5-0 \
        libopenjp2-7 \
        libpq5 \
        libproj25 \
        libsasl2-2 \
        libtiff6 \
        libwebp7 \
        libxml2 \
        libxslt1.1 \
        proj-data \
        proj-bin \
    ; \
    # Install PostgreSQL client
    echo 'deb https://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main' > /etc/apt/sources.list.d/postgresql.list; \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg; \
    apt-get update; \
    apt-get install -y --no-install-recommends postgresql-client-${PG_VERSION}; \
    # Apply latest security patches for OpenSSL
    apt-get upgrade -y libssl3 openssl

# Install wkhtmltopdf and geoipupdate (cache the downloads)
RUN --mount=type=cache,target=/tmp/downloads,sharing=locked \
    set -eux; \
    # wkhtmltopdf
    if [ "$TARGETARCH" = "arm64" ]; then \
        WKHTMLTOPDF_CHECKSUM=$WKHTMLTOPDF_ARM64_CHECKSUM; \
    elif [ "$TARGETARCH" = "amd64" ]; then \
        WKHTMLTOPDF_CHECKSUM=$WKHTMLTOPDF_AMD64_CHECKSUM; \
    else \
        echo "Unsupported architecture: $TARGETARCH" >&2; \
        exit 1; \
    fi; \
    WKHTMLTOPDF_DEB="/tmp/downloads/wkhtmltox_${WKHTMLTOPDF_VERSION}_${TARGETARCH}.deb"; \
    if [ ! -f "$WKHTMLTOPDF_DEB" ] || ! echo "${WKHTMLTOPDF_CHECKSUM} ${WKHTMLTOPDF_DEB}" | sha256sum -c - >/dev/null 2>&1; then \
        rm -f "$WKHTMLTOPDF_DEB"; \
        curl -fsSL -o "$WKHTMLTOPDF_DEB" \
            "https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTMLTOPDF_VERSION}-3/wkhtmltox_${WKHTMLTOPDF_VERSION}-3.bookworm_${TARGETARCH}.deb"; \
        echo "${WKHTMLTOPDF_CHECKSUM} ${WKHTMLTOPDF_DEB}" | sha256sum -c -; \
    fi; \
    apt-get install -y --no-install-recommends "$WKHTMLTOPDF_DEB"; \
    # geoipupdate
    if [ "$TARGETARCH" = "arm64" ]; then \
        GEOIP_CHECKSUM=$GEOIP_ARM64_CHECKSUM; \
    elif [ "$TARGETARCH" = "amd64" ]; then \
        GEOIP_CHECKSUM=$GEOIP_AMD64_CHECKSUM; \
    else \
        echo "Unsupported architecture for geoipupdate: $TARGETARCH" >&2; \
        exit 1; \
    fi; \
    GEOIP_DEB="/tmp/downloads/geoipupdate_${GEOIP_UPDATER_VERSION}_linux_${TARGETARCH}.deb"; \
    if [ ! -f "$GEOIP_DEB" ] || ! echo "${GEOIP_CHECKSUM} ${GEOIP_DEB}" | sha256sum -c - >/dev/null 2>&1; then \
        rm -f "$GEOIP_DEB"; \
        curl -fsSL -o "$GEOIP_DEB" \
            "https://github.com/maxmind/geoipupdate/releases/download/v${GEOIP_UPDATER_VERSION}/geoipupdate_${GEOIP_UPDATER_VERSION}_linux_${TARGETARCH}.deb"; \
        echo "${GEOIP_CHECKSUM} ${GEOIP_DEB}" | sha256sum -c -; \
    fi; \
    dpkg -i "$GEOIP_DEB"

# Create odoo user and directories
RUN set -eux; \
    groupadd -g ${GID} odoo; \
    useradd -l -m -d /home/odoo -s /bin/bash -u ${UID} -g ${GID} odoo; \
    mkdir -p /var/lib/odoo /mnt/extra-addons /etc/odoo; \
    chown -R odoo:odoo /var/lib/odoo /mnt/extra-addons /etc/odoo

# Copy virtual environment from builder (includes all pip packages)
COPY --from=builder /opt/venv /opt/venv

# Copy Odoo installation from builder
COPY --from=builder /opt/odoo /opt/odoo

# Copy OpenSPP and the OCA dependencies from builder
COPY --from=builder --chown=odoo:odoo /opt/extra-addons /mnt/extra-addons

# Configuration files
COPY docker/odoo.conf.template /etc/odoo/odoo.conf.template
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh; \
    chown odoo:odoo /etc/odoo/odoo.conf.template /entrypoint.sh

# Final configuration
WORKDIR /var/lib/odoo
VOLUME ["/var/lib/odoo"]
USER odoo

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=5 \
    CMD curl -f http://localhost:8069/web/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]

# =============================================================================
# Stage 3: Dev - For local development (dswd_* modules via volume mount)
# =============================================================================
# This is the image participants run. Their modules come from the volume mount
# at /mnt/extra-addons/custom - NOT copied into the image - so the container
# always runs the live code on disk. Everything else (OpenSPP, OCA deps,
# config, user) is inherited from the runtime stage.
FROM runtime AS dev
