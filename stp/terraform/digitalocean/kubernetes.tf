resource "digitalocean_kubernetes_cluster" "kubernetes_cluster" {
  name                 = var.k8s_cluster_name
  region               = var.do_region
  version              = var.k8s_cluster_version
  registry_integration = true
  vpc_uuid             = digitalocean_vpc.vpc.id
  depends_on = [
    digitalocean_vpc.vpc,
    digitalocean_container_registry.container_registry
  ]

  node_pool {
    name       = "${var.k8s_cluster_name}-default-pool"
    size       = var.k8s_node_size
    auto_scale = false
    node_count = var.k8s_node_count
  }
}

resource "kubernetes_namespace" "kubernetes_namespace" {
  metadata {
    name = var.k8s_namespace
  }

  depends_on = [digitalocean_kubernetes_cluster.kubernetes_cluster]
}

resource "kubernetes_secret" "kubernetes_secret_backend" {
  metadata {
    name      = var.k8s_secret_backend_name
    namespace = kubernetes_namespace.kubernetes_namespace.metadata[0].name
  }

  data = {
    ENV                  = var.k8s_secret_backend_data_env
    SECRET_KEY           = var.k8s_secret_backend_data_secret_key
    FRONTEND_URL         = var.k8s_secret_backend_data_frontend_url
    BACKEND_URL          = var.k8s_secret_backend_data_backend_url
    DATABASE_HOSTNAME    = digitalocean_database_cluster.database_cluster.host
    DATABASE_PORT        = digitalocean_database_cluster.database_cluster.port
    DATABASE_NAME        = digitalocean_database_db.database_db.name
    DATABASE_USERNAME    = digitalocean_database_user.database_user_backend.name
    DATABASE_PASSWORD    = digitalocean_database_user.database_user_backend.password
    S3_ACCESS_KEY_ID     = var.do_spaces_access_id
    S3_SECRET_ACCESS_KEY = var.do_spaces_secret_key
    S3_REGION_NAME       = digitalocean_spaces_bucket.bucket.region
    S3_ENDPOINT_URL      = digitalocean_spaces_bucket.bucket.endpoint
    S3_BUCKET_NAME       = digitalocean_spaces_bucket.bucket.name
  }
  depends_on = [
    kubernetes_namespace.kubernetes_namespace,
    digitalocean_database_cluster.database_cluster,
    digitalocean_database_user.database_user_backend
  ]
}