FROM traefik:v2.9

# Copy Traefik configuration
COPY traefik.yml /etc/traefik/
COPY config.yml /etc/traefik/

# Create directory for certificates
RUN mkdir -p /letsencrypt
