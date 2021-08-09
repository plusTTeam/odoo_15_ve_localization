FROM odoo:14
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip
RUN mkdir /coverage && mkdir /coverage/all && mkdir /coverage/local && chown -R odoo /coverage
RUN pip3 install pytest-odoo coverage pytest-html
USER odoo
