.
├── argocd
│   ├── applications
│   │   ├── elasticsearch.yaml
│   │   ├── kibana.yaml
│   │   ├── logstash.yaml
│   │   └── traefik.yaml
│   └── setup
│       └── argocd-installation.yaml
├── docker
│   ├── elasticsearch
│   │   └── Dockerfile
│   ├── kibana
│   │   └── Dockerfile
│   ├── logstash
│   │   └── Dockerfile
│   └── traefik
│       └── Dockerfile
├── documentation.md
├── elasticsearch-git.yaml
├── helm
│   ├── elasticsearch
│   │   ├── Chart.yaml
│   │   └── values.yaml
│   ├── kibana
│   │   ├── Chart.yaml
│   │   └── values.yaml
│   ├── logstash
│   │   ├── Chart.yaml
│   │   └── values.yaml
│   └── traefik
│       ├── Chart.yaml
│       └── values.yaml
├── kibana-git.yaml
├── logstash-git.yaml
├── traefik-git.yaml
└── utput

14 directories, 23 files
File: argocd/applications/elasticsearch.yaml
Lines: 23
-----BEGIN argocd/applications/elasticsearch.yaml-----
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: elasticsearch
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://helm.elastic.co
    chart: elasticsearch
    targetRevision: 7.17.3
    helm:
      valueFiles:
        - ../../helm/elasticsearch-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: elk
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

-----END argocd/applications/elasticsearch.yaml-----

File: argocd/applications/kibana.yaml
Lines: 23
-----BEGIN argocd/applications/kibana.yaml-----
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kibana
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://helm.elastic.co
    chart: kibana
    targetRevision: 7.17.3
    helm:
      valueFiles:
        - ../../helm/kibana-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: elk
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

-----END argocd/applications/kibana.yaml-----

File: argocd/applications/logstash.yaml
Lines: 23
-----BEGIN argocd/applications/logstash.yaml-----
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: logstash
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://helm.elastic.co
    chart: logstash
    targetRevision: 7.17.3
    helm:
      valueFiles:
        - ../../helm/logstash-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: elk
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

-----END argocd/applications/logstash.yaml-----

File: argocd/applications/traefik.yaml
Lines: 23
-----BEGIN argocd/applications/traefik.yaml-----
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: traefik
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://helm.traefik.io/traefik
    chart: traefik
    targetRevision: 10.24.0
    helm:
      valueFiles:
        - ../../helm/traefik-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: traefik
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

-----END argocd/applications/traefik.yaml-----

File: argocd/setup/argocd-installation.yaml
Lines: 8
-----BEGIN argocd/setup/argocd-installation.yaml-----
# argocd/setup/argocd-installation.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: argocd
---
# This includes the core ArgoCD installation
# When applying, use: kubectl apply -f argocd-installation.yaml -n argocd

-----END argocd/setup/argocd-installation.yaml-----

File: elasticsearch-git.yaml
Lines: 23
-----BEGIN elasticsearch-git.yaml-----
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: elasticsearch
  namespace: argocd
spec:
  project: default
  source:
    repoURL: git@github.com:wrightpt/elk-stack-kubernetes-simplified.git
    targetRevision: main
    path: helm
    helm:
      valueFiles:
        - elasticsearch-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: elk
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

-----END elasticsearch-git.yaml-----

File: helm/elasticsearch/Chart.yaml
Lines: 10
-----BEGIN helm/elasticsearch/Chart.yaml-----
apiVersion: v2
name: elasticsearch
description: Elasticsearch Helm chart for Kubernetes
type: application
version: 1.0.0
appVersion: 7.17.3
dependencies:
  - name: elasticsearch
    version: 7.17.3
    repository: https://helm.elastic.co

-----END helm/elasticsearch/Chart.yaml-----

File: helm/elasticsearch/values.yaml
Lines: 35
-----BEGIN helm/elasticsearch/values.yaml-----
# helm/elasticsearch-values.yaml
replicas: 1  # Adjust based on your home server capacity

# Resource requests and limits
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "1"
    memory: "2Gi"

# Persistence configuration
persistence:
  enabled: true
  storageClass: "local-storage"
  size: "30Gi"

# Network settings
service:
  type: ClusterIP

# Security settings
securityContext:
  enabled: true
  runAsUser: 1000
  fsGroup: 1000

# Config for ES
esConfig:
  elasticsearch.yml: |
    cluster.name: home-cluster
    discovery.type: single-node
    xpack.security.enabled: true
    xpack.security.transport.ssl.enabled: true

-----END helm/elasticsearch/values.yaml-----

File: helm/kibana/Chart.yaml
Lines: 10
-----BEGIN helm/kibana/Chart.yaml-----
apiVersion: v2
name: kibana
description: Kibana Helm chart for Kubernetes
type: application
version: 1.0.0
appVersion: 7.17.3
dependencies:
  - name: kibana
    version: 7.17.3
    repository: https://helm.elastic.co

-----END helm/kibana/Chart.yaml-----

File: helm/kibana/values.yaml
Lines: 67
-----BEGIN helm/kibana/values.yaml-----
# helm/kibana-values.yaml
image:
  repository: "kibana"
  tag: "7.17.3"

elasticsearchHosts: "http://elasticsearch-master:9200"

# Resource requests and limits
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
  limits:
    cpu: "1"
    memory: "2Gi"

# Persistence configuration
persistence:
  enabled: true
  storageClass: "local-storage"
  size: "5Gi"

# Network settings
service:
  type: ClusterIP
  port: 5601

# Security settings
securityContext:
  enabled: true
  runAsUser: 1000
  fsGroup: 1000

# Kibana configuration
kibanaConfig:
  kibana.yml: |
    server.host: "0.0.0.0"
    server.publicBaseUrl: "https://kibana.1xmr.com"
    elasticsearch.username: "kibana_admin"
    elasticsearch.password: "${KIBANA_ES_PASSWORD}"
    elasticsearch.ssl.verificationMode: none
    xpack.encryptedSavedObjects.encryptionKey: "${KIBANA_ENCRYPTION_KEY}"
    logging:
      appenders:
        file:
          type: file
          fileName: /var/log/kibana/kibana.log
          layout:
            type: json
      root:
        appenders:
          - default
          - file
    pid.file: /run/kibana/kibana.pid

# Environment variables for secrets
extraEnvs:
  - name: KIBANA_ES_PASSWORD
    valueFrom:
      secretKeyRef:
        name: kibana-credentials
        key: password
  - name: KIBANA_ENCRYPTION_KEY
    valueFrom:
      secretKeyRef:
        name: kibana-credentials
        key: encryptionKey

-----END helm/kibana/values.yaml-----

File: helm/logstash/Chart.yaml
Lines: 10
-----BEGIN helm/logstash/Chart.yaml-----
apiVersion: v2
name: logstash
description: Logstash Helm chart for Kubernetes
type: application
version: 1.0.0
appVersion: 7.17.3
dependencies:
  - name: logstash
    version: 7.17.3
    repository: https://helm.elastic.co

-----END helm/logstash/Chart.yaml-----

File: helm/logstash/values.yaml
Lines: 119
-----BEGIN helm/logstash/values.yaml-----
# helm/logstash-values.yaml
image:
  repository: "logstash"
  tag: "7.17.3"

# Resource requests and limits
resources:
  requests:
    cpu: "500m"
    memory: "2Gi"
  limits:
    cpu: "2"
    memory: "4Gi"

# Persistence configuration
persistence:
  enabled: true
  storageClass: "local-storage"
  size: "10Gi"

# Network settings
service:
  type: ClusterIP
  ports:
    - name: http
      port: 5044
      protocol: TCP

# Security settings
securityContext:
  runAsUser: 1000
  fsGroup: 1000

# Logstash configuration
logstashConfig:
  logstash.yml: |
    path.data: /usr/share/logstash/data
    path.logs: /var/log/logstash
    node.name: nextjs-market-logstash
    pipeline.workers: 8
    pipeline.batch.size: 1000
    pipeline.batch.delay: 50
    queue.type: persisted
    queue.max_bytes: 3gb
    log.level: debug

  pipelines.yml: |
    - pipeline.id: main
      path.config: "/usr/share/logstash/pipeline/*.conf"

# JVM options
logstashJavaOpts: "-Xms2g -Xmx2g"

# Pipeline configuration
logstashPipeline:
  nextjs-market.conf: |
    input {
      http {
        host => "0.0.0.0"
        port => 5044
        codec => json
        
        response_headers => {
          "Content-Type" => "application/json"
          "Access-Control-Allow-Origin" => "*"
          "Access-Control-Allow-Methods" => "POST, OPTIONS"
          "Access-Control-Allow-Headers" => "Content-Type"
        }
      }
    }

    filter {
      mutate {
        add_field => {
          "received_at" => "%{@timestamp}"
          "environment" => "${ENVIRONMENT}"
          "service" => "nextjs-market"
          "log_type" => "application"
        }
        remove_field => ["headers", "password"]
      }
    }

    output {
      elasticsearch {
        hosts => ["${ES_HOSTS}"]
        user => "${ES_USER}"
        password => "${ES_PASSWORD}"
        index => "nextjs-market-${ENVIRONMENT}-%{+YYYY.MM.dd}"
        ssl_verification_mode => "none"
        timeout => 120
        retry_on_conflict => 5
        retry_max_interval => 30
        retry_initial_interval => 2
      }
      
      file {
        path => "/var/log/logstash/nextjs-market-debug.log"
        codec => json_lines
        flush_interval => 60
      }
    }

# Environment variables
extraEnvs:
  - name: ES_HOSTS
    value: "https://elasticsearch-master:9200"
  - name: ES_USER
    valueFrom:
      secretKeyRef:
        name: logstash-credentials
        key: username
  - name: ES_PASSWORD
    valueFrom:
      secretKeyRef:
        name: logstash-credentials
        key: password
  - name: ENVIRONMENT
    value: "production"

-----END helm/logstash/values.yaml-----

File: helm/traefik/Chart.yaml
Lines: 10
-----BEGIN helm/traefik/Chart.yaml-----
apiVersion: v2
name: traefik
description: Traefik Helm chart for Kubernetes
type: application
version: 1.0.0
appVersion: 10.24.0
dependencies:
  - name: traefik
    version: 10.24.0
    repository: https://helm.traefik.io/traefik

-----END helm/traefik/Chart.yaml-----

File: helm/traefik/values.yaml
Lines: 146
-----BEGIN helm/traefik/values.yaml-----
# helm/traefik-values.yaml
image:
  name: traefik
  tag: v2.9

# Use ingressRoute instead of the deprecated ingress
ingressRoute:
  dashboard:
    enabled: true

# Configuration
additionalArguments:
  - "--providers.file.filename=/etc/traefik/config.yml"
  - "--providers.file.watch=true"
  - "--log.level=DEBUG"
  - "--certificatesresolvers.letsencrypt.acme.email=connect@3xmr.com"
  - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
  - "--certificatesresolvers.letsencrypt.acme.caserver=https://acme-v02.api.letsencrypt.org/directory"
  - "--certificatesresolvers.letsencrypt.acme.dnschallenge.provider=cloudflare"
  - "--certificatesresolvers.letsencrypt.acme.dnschallenge.delaybeforecheck=30"
  - "--serverstransport.insecureskipverify=true"

# Define entry points
ports:
  web:
    redirectTo: websecure
    port: 80
    expose: true
    exposedPort: 80
  websecure:
    port: 443
    expose: true
    exposedPort: 443
    tls:
      enabled: true
  traefik:
    port: 8080
    expose: true
    exposedPort: 8080

# Persistent volumes for certificates
persistence:
  enabled: true
  name: letsencrypt
  accessMode: ReadWriteOnce
  size: 128Mi
  storageClass: "local-storage"
  path: /letsencrypt

# Mount configuration file
deployment:
  additionalVolumes:
    - name: traefik-config
      configMap:
        name: traefik-config
  additionalVolumeMounts:
    - name: traefik-config
      mountPath: /etc/traefik/config.yml
      subPath: config.yml

# Additional configuration
additionalResources:
  - apiVersion: v1
    kind: ConfigMap
    metadata:
      name: traefik-config
    data:
      config.yml: |
        http:
          routers:
            rpc:
              rule: "Host(`rpc.1xmr.com`)"
              entryPoints:
                - websecure
              service: rpc
              tls:
                certResolver: letsencrypt
            wallet:
              rule: "Host(`wallet.1xmr.com`)"
              entryPoints:
                - websecure
              service: wallet
              tls:
                certResolver: letsencrypt
            kibana:
              rule: "Host(`kibana.1xmr.com`)"
              entryPoints:
                - websecure
              service: kibana
              tls:
                certResolver: letsencrypt
            elasticsearch:
              rule: "Host(`elasticsearch.1xmr.com`)"
              entryPoints:
                - websecure
              service: elasticsearch
              tls:
                certResolver: letsencrypt
              middlewares:
                - es-auth
            logstash:
              rule: "Host(`logstash.1xmr.com`)"
              entryPoints:
                - websecure
              service: logstash
              tls:
                certResolver: letsencrypt
          services:
            rpc:
              loadBalancer:
                servers:
                  - url: "http://rpc-service:18082"
                passHostHeader: true
            wallet:
              loadBalancer:
                servers:
                  - url: "http://wallet-service:18081"
                passHostHeader: true
            kibana:
              loadBalancer:
                servers:
                  - url: "http://kibana:5601"
                passHostHeader: true
            elasticsearch:
              loadBalancer:
                servers:
                  - url: "http://elasticsearch-master:9200"
                passHostHeader: true
            logstash:
              loadBalancer:
                servers:
                  - url: "http://logstash:5044"
                passHostHeader: true
          middlewares:
            es-auth:
              headers:
                customRequestHeaders:
                  Authorization: "Basic ${ES_AUTH_HEADER}"

# Environment variables for secrets
env:
  - name: ES_AUTH_HEADER
    valueFrom:
      secretKeyRef:
        name: es-auth-header
        key: value

-----END helm/traefik/values.yaml-----

File: kibana-git.yaml
Lines: 23
-----BEGIN kibana-git.yaml-----
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kibana
  namespace: argocd
spec:
  project: default
  source:
    repoURL: git@github.com:wrightpt/elk-stack-kubernetes-simplified.git
    targetRevision: main
    path: helm
    helm:
      valueFiles:
        - kibana-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: elk
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

-----END kibana-git.yaml-----

File: logstash-git.yaml
Lines: 23
-----BEGIN logstash-git.yaml-----
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: logstash
  namespace: argocd
spec:
  project: default
  source:
    repoURL: git@github.com:wrightpt/elk-stack-kubernetes-simplified.git
    targetRevision: main
    path: helm
    helm:
      valueFiles:
        - logstash-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: elk
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

-----END logstash-git.yaml-----

File: traefik-git.yaml
Lines: 23
-----BEGIN traefik-git.yaml-----
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: traefik
  namespace: argocd
spec:
  project: default
  source:
    repoURL: git@github.com:wrightpt/elk-stack-kubernetes-simplified.git
    targetRevision: main
    path: helm
    helm:
      valueFiles:
        - traefik-values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: traefik
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

-----END traefik-git.yaml-----

