variable "location" {
  description = "Azure region to deploy resources into"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the Azure Resource Group (overrides auto-generated name if set)"
  type        = string
  default     = ""
}

variable "aks_vm_size" {
  description = "VM size for AKS default node pool"
  type        = string
  default     = "Standard_D2s_v3"
}

variable "node_count" {
  description = "Number of nodes in the AKS default node pool"
  type        = number
  default     = 2
}

variable "db_username" {
  description = "Administrator login for PostgreSQL Flexible Server"
  type        = string
  default     = "signalharbor"
}

variable "db_password" {
  description = "Administrator password for PostgreSQL Flexible Server"
  type        = string
  sensitive   = true
}

variable "db_storage_mb" {
  description = "Storage size in MB for PostgreSQL Flexible Server"
  type        = number
  default     = 32768
}

variable "db_sku" {
  description = "SKU name for PostgreSQL Flexible Server"
  type        = string
  default     = "B_Standard_B1ms"
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
