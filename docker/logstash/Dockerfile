FROM docker.elastic.co/logstash/logstash:7.17.3

# Copy configuration files
COPY logstash.yml /usr/share/logstash/config/
COPY pipelines.yml /usr/share/logstash/config/
COPY jvm.options /usr/share/logstash/config/
COPY conf.d/ /usr/share/logstash/pipeline/

# Set permissions
USER root
RUN chmod 660 /usr/share/logstash/config/logstash.yml \
    && chmod 660 /usr/share/logstash/config/pipelines.yml \
    && chmod 660 /usr/share/logstash/config/jvm.options \
    && chmod -R 660 /usr/share/logstash/pipeline/ \
    && chown -R 1000:0 /usr/share/logstash/config \
    && chown -R 1000:0 /usr/share/logstash/pipeline

# Switch back to logstash user
USER 1000
