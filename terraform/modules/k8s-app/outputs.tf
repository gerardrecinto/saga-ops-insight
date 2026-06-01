output "namespace" {
  description = "Kubernetes namespace where Signal Harbor is deployed"
  value       = kubernetes_namespace.signalharbor.metadata[0].name
}

output "deployment_name" {
  description = "Name of the Kubernetes Deployment"
  value       = kubernetes_deployment.signalharbor.metadata[0].name
}

output "service_name" {
  description = "Name of the Kubernetes Service"
  value       = kubernetes_service.signalharbor.metadata[0].name
}

output "ingress_host" {
  description = "Hostname configured on the Ingress resource"
  value       = var.ingress_host
}
