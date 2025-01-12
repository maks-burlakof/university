variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "do_spaces_access_id" {
  description = "DigitalOcean Spaces access key"
  type        = string
  sensitive   = true
}

variable "do_spaces_secret_key" {
  description = "DigitalOcean Spaces secret key"
  type        = string
  sensitive   = true
}

variable "do_region" {
  description = "The digital ocean region slug for where to create all resources"
  type        = string
  default     = "fra1"
}

variable "vpc_name" {
  description = "The name of the VPC"
  type        = string
  default     = "stp-babushka-vpc"
}

variable "proj_name" {
  description = "The name of the project"
  type        = string
}

variable "proj_env" {
  description = "The environment of the project"
  type        = string
  validation {
    condition     = contains(["Development", "Staging", "Production"], var.proj_env)
    error_message = "The project environment must be one of: Development, Staging, Production"
  }
}

variable "creg_name" {
  description = "The name of the Container Registry"
  type        = string
}

variable "creg_size" {
  description = "The subscription tier slug for the Container Registry"
  type        = string
  default     = "basic"
}

variable "k8s_cluster_name" {
  description = "The name of the kubernetes cluster"
  type        = string
}

variable "k8s_cluster_version" {
  description = "Version of the kubernetes cluster"
  type        = string
  default     = "1.31.1-do.4"
}

variable "k8s_node_count" {
  description = "The number of nodes in the default pool"
  type        = number
  default     = 1
}

variable "k8s_node_size" {
  description = "The node machine type slug for each node in the default pool"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "k8s_namespace" {
  description = "The name of the kubernetes namespace"
  type        = string
}

variable "k8s_secret_backend_name" {
  description = "The name of the kubernetes backend secret"
  type        = string
  default     = "backend-secrets"
}

variable "k8s_secret_backend_data_env" {
  description = "The ENV environment variable for the kubernetes backend secret"
  type        = string
}

variable "k8s_secret_backend_data_secret_key" {
  description = "The SECRET_KEY environment variable for the kubernetes backend secret"
  type        = string
}

variable "k8s_secret_backend_data_backend_url" {
  description = "The BACKEND_URL environment variable for the kubernetes backend secret"
  type        = string
}

variable "k8s_secret_backend_data_frontend_url" {
  description = "The FRONTEND_URL environment variable for the kubernetes backend secret"
  type        = string
}

variable "db_cluster_name" {
  description = "Cluster name of the Database service"
  type        = string
}

variable "db_cluster_size" {
  description = "Cluster size of the Database service"
  type        = string
  default     = "db-s-1vcpu-1gb"
}

variable "db_database_name" {
  description = "Name of the database inside the cluster"
  type        = string
}

variable "db_database_user_backend_name" {
  description = "Database user for the backend service"
  type        = string
}

variable "db_database_user_localmanagement_name" {
  description = "Database user for the management purposes"
  type        = string
}

variable "bucket_name" {
  description = "The name of the object storage bucket"
  type        = string
}