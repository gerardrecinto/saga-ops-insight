output "metallb_pool_name" {
  description = "Name of the MetalLB IPAddressPool created for Signal Harbor"
  value       = "signalharbor-pool"
}

output "vip_address" {
  description = "Citrix ADC virtual IP address for Signal Harbor"
  value       = var.vip_address
}

output "metallb_assigned_range" {
  description = "IP range assigned to the MetalLB address pool"
  value       = var.metallb_ip_range
}

output "service_endpoint" {
  description = "HTTPS endpoint for the Signal Harbor service via the VIP"
  value       = "https://${var.vip_address}"
}
