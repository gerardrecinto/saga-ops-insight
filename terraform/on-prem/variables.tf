variable "kubeconfig_path" {
  description = "Absolute path to the kubeconfig file for the on-prem Kubernetes cluster"
  type        = string
}

variable "metallb_ip_range" {
  description = "IP address range MetalLB will allocate from (e.g. '192.168.1.200-192.168.1.250')"
  type        = string
  default     = "192.168.1.200-192.168.1.250"
}

variable "vip_address" {
  description = "Virtual IP address for the Citrix ADC load balancer vserver"
  type        = string
}

variable "netscaler_endpoint" {
  description = "HTTPS URL of the Citrix ADC NITRO API endpoint (e.g. 'https://192.168.1.1')"
  type        = string
}

variable "netscaler_username" {
  description = "Citrix ADC NITRO API username"
  type        = string
  sensitive   = true
}

variable "netscaler_password" {
  description = "Citrix ADC NITRO API password"
  type        = string
  sensitive   = true
}

variable "backend_replica_count" {
  description = "Number of backend service bindings to create on the Citrix ADC"
  type        = number
  default     = 2
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

variable "app_version" {
  description = "Docker image tag to deploy"
  type        = string
}

variable "database_url" {
  description = "PostgreSQL connection URL for the on-prem database"
  type        = string
  sensitive   = true
}

variable "redis_url" {
  description = "Redis connection URL for the on-prem Redis instance"
  type        = string
  sensitive   = true
}
