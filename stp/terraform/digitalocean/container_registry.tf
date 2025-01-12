resource "digitalocean_container_registry" "container_registry" {
  name                   = var.creg_name
  subscription_tier_slug = var.creg_size
  region                 = var.do_region
}