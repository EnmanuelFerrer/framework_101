FROM odoo:19.0

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends unzip \
    && pip3 install ruff --break-system-packages \
    && rm -rf /var/lib/apt/lists/*

USER odoo
