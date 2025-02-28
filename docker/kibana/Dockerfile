FROM docker.elastic.co/kibana/kibana:7.17.3

# Copy custom configuration
COPY kibana.yml /usr/share/kibana/config/

# Set permissions
USER root
RUN chmod 660 /usr/share/kibana/config/kibana.yml \
    && chown -R 1000:0 /usr/share/kibana/config

# Switch back to kibana user
USER 1000
