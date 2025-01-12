terraform {
  cloud {
    organization = "maks-burlakof-org"

    workspaces {
      name = "prod"
    }
  }
}

module "digitalocean" {
  source = "./digitalocean"

  do_token                              = var.do_token
  do_spaces_access_id                   = var.do_spaces_access_id
  do_spaces_secret_key                  = var.do_spaces_secret_key
  proj_name                             = var.do_proj_name
  proj_env                              = var.do_proj_env
  creg_name                             = "containerregistry-registry"
  k8s_cluster_name                      = "kubernetes-cluster"
  k8s_namespace                         = var.k8s_namespace
  k8s_secret_backend_data_env           = var.k8s_secret_backend_data_env
  k8s_secret_backend_data_secret_key    = var.k8s_secret_backend_data_secret_key
  k8s_secret_backend_data_backend_url   = var.k8s_secret_backend_data_backend_url
  k8s_secret_backend_data_frontend_url  = var.k8s_secret_backend_data_frontend_url
  db_cluster_name                       = "db-postgresql"
  db_database_name                      = var.db_name
  db_database_user_backend_name         = var.db_user_backend_name
  db_database_user_localmanagement_name = var.db_user_localmanagement_name
  bucket_name                           = var.bucket_name
}