resource "kubernetes_namespace" "signalharbor" {
  metadata {
    name = var.namespace
    labels = {
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }
}

resource "kubernetes_secret" "signalharbor_secrets" {
  metadata {
    name      = "signalharbor-secrets"
    namespace = kubernetes_namespace.signalharbor.metadata[0].name
  }

  data = {
    api_key      = var.api_key
    database_url = var.database_url
    redis_url    = var.redis_url
  }

  type = "Opaque"
}

resource "kubernetes_deployment" "signalharbor" {
  metadata {
    name      = "signalharbor"
    namespace = kubernetes_namespace.signalharbor.metadata[0].name
    labels = {
      "app.kubernetes.io/name"       = "signalharbor"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "signalharbor"
      }
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name" = "signalharbor"
        }
      }

      spec {
        container {
          name  = "signalharbor"
          image = var.image

          port {
            container_port = var.app_port
            protocol       = "TCP"
          }

          env {
            name = "API_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.signalharbor_secrets.metadata[0].name
                key  = "api_key"
              }
            }
          }

          env {
            name = "DATABASE_URL"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.signalharbor_secrets.metadata[0].name
                key  = "database_url"
              }
            }
          }

          env {
            name = "REDIS_URL"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.signalharbor_secrets.metadata[0].name
                key  = "redis_url"
              }
            }
          }

          env {
            name  = "RISK_LOOKBACK_HOURS"
            value = tostring(var.risk_lookback_hours)
          }

          env {
            name  = "CACHE_TTL_SECONDS"
            value = tostring(var.cache_ttl_seconds)
          }

          resources {
            requests = {
              cpu    = var.cpu_request
              memory = var.memory_request
            }
            limits = {
              cpu    = var.cpu_limit
              memory = var.memory_limit
            }
          }

          readiness_probe {
            http_get {
              path = "/health"
              port = var.app_port
            }
            initial_delay_seconds = 10
            period_seconds        = 10
            failure_threshold     = 3
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = var.app_port
            }
            initial_delay_seconds = 30
            period_seconds        = 15
            failure_threshold     = 3
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "signalharbor" {
  metadata {
    name      = "signalharbor"
    namespace = kubernetes_namespace.signalharbor.metadata[0].name
    labels = {
      "app.kubernetes.io/name"       = "signalharbor"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  spec {
    selector = {
      "app.kubernetes.io/name" = "signalharbor"
    }

    type = "ClusterIP"

    port {
      port        = 80
      target_port = var.app_port
      protocol    = "TCP"
    }
  }
}

resource "kubernetes_ingress_v1" "signalharbor" {
  metadata {
    name      = "signalharbor"
    namespace = kubernetes_namespace.signalharbor.metadata[0].name
    annotations = {
      "kubernetes.io/ingress.class"                    = "nginx"
      "nginx.ingress.kubernetes.io/ssl-redirect"       = "true"
      "cert-manager.io/cluster-issuer"                 = "letsencrypt-prod"
      "nginx.ingress.kubernetes.io/proxy-body-size"    = "16m"
      "nginx.ingress.kubernetes.io/proxy-read-timeout" = "60"
    }
    labels = {
      "app.kubernetes.io/name"       = "signalharbor"
      "app.kubernetes.io/managed-by" = "terraform"
    }
  }

  spec {
    tls {
      hosts       = [var.ingress_host]
      secret_name = "signalharbor-tls"
    }

    rule {
      host = var.ingress_host

      http {
        path {
          path      = "/"
          path_type = "Prefix"

          backend {
            service {
              name = kubernetes_service.signalharbor.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}
