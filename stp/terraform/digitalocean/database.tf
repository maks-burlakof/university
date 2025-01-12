resource "digitalocean_database_cluster" "database_cluster" {
  name                 = var.db_cluster_name
  engine               = "pg"
  version              = "16"
  size                 = var.db_cluster_size
  region               = var.do_region
  node_count           = 1
  private_network_uuid = digitalocean_vpc.vpc.id
  depends_on           = [digitalocean_vpc.vpc]
}

resource "digitalocean_database_db" "database_db" {
  cluster_id = digitalocean_database_cluster.database_cluster.id
  name       = var.db_database_name
  depends_on = [digitalocean_database_cluster.database_cluster]
}

resource "digitalocean_database_user" "database_user_backend" {
  cluster_id = digitalocean_database_cluster.database_cluster.id
  name       = var.db_database_user_backend_name
  depends_on = [digitalocean_database_cluster.database_cluster]
}

resource "digitalocean_database_user" "database_user_localmanagement" {
  cluster_id = digitalocean_database_cluster.database_cluster.id
  name       = var.db_database_user_localmanagement_name
  depends_on = [digitalocean_database_cluster.database_cluster]
}

resource "postgresql_grant" "database_user_backend_grant" {
  role        = digitalocean_database_user.database_user_backend.name
  database    = digitalocean_database_db.database_db.name
  schema      = "public"
  object_type = "table"
  privileges  = ["SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "REFERENCES", "TRIGGER"]
  depends_on = [
    digitalocean_database_user.database_user_backend,
    digitalocean_database_db.database_db
  ]
}

resource "postgresql_grant" "database_user_localmanagement_grant" {
  role        = digitalocean_database_user.database_user_localmanagement.name
  database    = digitalocean_database_db.database_db.name
  schema      = "public"
  object_type = "table"
  privileges  = ["SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "REFERENCES", "TRIGGER"]
  depends_on = [
    digitalocean_database_user.database_user_localmanagement,
    digitalocean_database_db.database_db
  ]
}