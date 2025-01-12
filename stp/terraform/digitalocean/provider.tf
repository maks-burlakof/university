terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.43.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.33.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "2.16.1"
    }
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "1.24.0"
    }
  }
}

provider "digitalocean" {
  token             = var.do_token
  spaces_access_id  = var.do_spaces_access_id
  spaces_secret_key = var.do_spaces_secret_key
}

provider "kubernetes" {
  host  = digitalocean_kubernetes_cluster.kubernetes_cluster.endpoint
  token = digitalocean_kubernetes_cluster.kubernetes_cluster.kube_config[0].token
  cluster_ca_certificate = base64decode(
    digitalocean_kubernetes_cluster.kubernetes_cluster.kube_config[0].cluster_ca_certificate
  )
}

provider "helm" {
  kubernetes {
    host  = digitalocean_kubernetes_cluster.kubernetes_cluster.endpoint
    token = digitalocean_kubernetes_cluster.kubernetes_cluster.kube_config[0].token
    cluster_ca_certificate = base64decode(
      digitalocean_kubernetes_cluster.kubernetes_cluster.kube_config[0].cluster_ca_certificate
    )
  }
}

provider "postgresql" {
  host     = digitalocean_database_cluster.database_cluster.host
  port     = digitalocean_database_cluster.database_cluster.port
  database = digitalocean_database_cluster.database_cluster.database
  username = digitalocean_database_cluster.database_cluster.user
  password = digitalocean_database_cluster.database_cluster.password
  sslmode  = "require"
}