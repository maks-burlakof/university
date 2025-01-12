resource "digitalocean_vpc" "vpc" {
  name   = var.vpc_name
  region = var.do_region
}