variable "region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "node_max" {
  description = "Maximum number of EKS managed nodes"
  type        = number
  default     = 5
}

variable "node_desired" {
  description = "Desired number of EKS managed nodes"
  type        = number
  default     = 2
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_storage_gb" {
  description = "Allocated storage for RDS in GB"
  type        = number
  default     = 20
}

variable "db_username" {
  description = "Master username for the RDS PostgreSQL instance"
  type        = string
  default     = "signalharbor"
}

variable "db_password" {
  description = "Master password for the RDS PostgreSQL instance"
  type        = string
  sensitive   = true
}

variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.micro"
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
