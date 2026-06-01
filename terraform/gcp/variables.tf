variable "project_id" {
  description = "GCP project ID where all resources will be created"
  type        = string
}

variable "region" {
  description = "GCP region to deploy resources into"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)"
  type        = string
}

variable "cluster_name" {
  description = "Name override for the GKE cluster (defaults to signalharbor-{environment})"
  type        = string
  default     = ""
}

variable "db_tier" {
  description = "Cloud SQL machine tier"
  type        = string
  default     = "db-f1-micro"
}

variable "db_disk_gb" {
  description = "Cloud SQL disk size in GB"
  type        = number
  default     = 20
}

variable "db_username" {
  description = "PostgreSQL database username"
  type        = string
  default     = "signalharbor"
}

variable "db_password" {
  description = "PostgreSQL database password"
  type        = string
  sensitive   = true
}

variable "redis_memory_gb" {
  description = "Memory size in GB for the Memorystore Redis instance"
  type        = number
  default     = 1
}

variable "app_version" {
  description = "Docker image tag to deploy"
  type        = string
}

variable "api_key" {
  description = "API key for Signal Harbor application"
  type        = string
  sensitive   = true
}

variable "ingress_host" {
  description = "Hostname for the Kubernetes Ingress (e.g. signalharbor.example.com)"
  type        = string
}
