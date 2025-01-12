resource "digitalocean_project" "project" {
  name        = var.proj_name
  description = "University project Babushka - social network for publishing photos, inspired by Instagram."
  purpose     = "Web Application"
  environment = var.proj_env
  resources = [
    digitalocean_database_cluster.database_cluster.urn,
    digitalocean_kubernetes_cluster.kubernetes_cluster.urn,
    digitalocean_spaces_bucket.bucket.urn,
  ]
}