resource "digitalocean_spaces_bucket" "bucket" {
  name   = var.bucket_name
  region = var.do_region
  acl    = "private"
}