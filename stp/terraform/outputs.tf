output "db_cluster_host" {
  value       = module.digitalocean.db_cluster_host
  description = "The host of the database cluster"
}

output "db_cluster_port" {
  value       = module.digitalocean.db_cluster_port
  description = "The port of the database cluster"
}

output "db_user_backend_password" {
  value       = module.digitalocean.db_user_backend_password
  description = "Backend database user password"
  sensitive   = true
}

output "db_user_localmanagement_password" {
  value       = module.digitalocean.db_user_localmanagement_password
  description = "Localmanagement database user password"
  sensitive   = true
}

output "creg_endpoint" {
  value       = module.digitalocean.creg_endpoint
  description = "The endpoint of the container registry"
}

output "k8s_cluster_ipv4_address" {
  value       = module.digitalocean.k8s_cluster_ipv4_address
  description = "The public IPv4 address of the Kubernetes master node"
}

output "bucket_domain_name" {
  value       = module.digitalocean.bucket_domain_name
  description = "The domain of the object storage bucket"
}