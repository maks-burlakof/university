output "db_cluster_host" {
  value       = digitalocean_database_cluster.database_cluster.host
  description = "The host of the database cluster"
}

output "db_cluster_port" {
  value       = digitalocean_database_cluster.database_cluster.port
  description = "The port of the database cluster"
}

output "db_user_backend_password" {
  value       = digitalocean_database_user.database_user_backend.password
  description = "Backend database user password"
  sensitive   = true
}

output "db_user_localmanagement_password" {
  value       = digitalocean_database_user.database_user_localmanagement.password
  description = "Localmanagement database user password"
  sensitive   = true
}

output "creg_endpoint" {
  value       = digitalocean_container_registry.container_registry.endpoint
  description = "The endpoint of the container registry"
}

output "k8s_cluster_ipv4_address" {
  value       = digitalocean_kubernetes_cluster.kubernetes_cluster.ipv4_address
  description = "The public IPv4 address of the Kubernetes master node"
}

output "bucket_domain_name" {
  value       = digitalocean_spaces_bucket.bucket.bucket_domain_name
  description = "The domain of the object storage bucket"
}