output "cluster_endpoint" {
  description = "GKE cluster API server endpoint"
  value       = "https://${google_container_cluster.signalharbor.endpoint}"
}

output "db_connection_name" {
  description = "Cloud SQL instance connection name (project:region:instance)"
  value       = google_sql_database_instance.signalharbor.connection_name
}

output "db_instance_name" {
  description = "Cloud SQL instance name"
  value       = google_sql_database_instance.signalharbor.name
}

output "redis_host" {
  description = "Memorystore Redis host IP"
  value       = google_redis_instance.signalharbor.host
}

output "redis_port" {
  description = "Memorystore Redis port"
  value       = google_redis_instance.signalharbor.port
}

output "configure_kubectl_cmd" {
  description = "gcloud command to configure kubectl for this cluster"
  value       = "gcloud container clusters get-credentials ${google_container_cluster.signalharbor.name} --region ${var.region} --project ${var.project_id}"
}
