FROM docker.elastic.co/elasticsearch/elasticsearch:7.17.3

# Copy custom configuration files
COPY elasticsearch.yml /usr/share/elasticsearch/config/
COPY jvm.options /usr/share/elasticsearch/config/

# Set permissions
USER root
RUN chmod 660 /usr/share/elasticsearch/config/elasticsearch.yml \
    && chmod 660 /usr/share/elasticsearch/config/jvm.options \
    && chown -R 1000:0 /usr/share/elasticsearch/config

# Switch back to elasticsearch user
USER 1000
