output "aks_kube_config" {
  description = "Raw kubeconfig for the AKS cluster"
  value       = azurerm_kubernetes_cluster.signalharbor.kube_config_raw
  sensitive   = true
}

output "resource_group_name" {
  description = "Name of the Azure Resource Group containing all resources"
  value       = azurerm_resource_group.signalharbor.name
}

output "db_fqdn" {
  description = "Fully qualified domain name of the PostgreSQL Flexible Server"
  value       = azurerm_postgresql_flexible_server.signalharbor.fqdn
}

output "redis_hostname" {
  description = "Hostname of the Azure Redis Cache instance"
  value       = azurerm_redis_cache.signalharbor.hostname
}

output "redis_port" {
  description = "SSL port for the Azure Redis Cache instance"
  value       = azurerm_redis_cache.signalharbor.ssl_port
}

output "redis_primary_key" {
  description = "Primary access key for the Azure Redis Cache instance"
  value       = azurerm_redis_cache.signalharbor.primary_access_key
  sensitive   = true
}
