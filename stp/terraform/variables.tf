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

variable "do_proj_name" {
  description = "The name of the DigitalOcean project"
  type        = string
}

variable "do_proj_env" {
  description = "The environment of the DigitalOcean project"
  type        = string
  validation {
    condition     = contains(["Development", "Staging", "Production"], var.do_proj_env)
    error_message = "The project environment must be one of: Development, Staging, Production"
  }
}

variable "k8s_namespace" {
  description = "The name of the kubernetes namespace"
  type        = string
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

variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "db_user_backend_name" {
  description = "Database user for the backend service"
  type        = string
}

variable "db_user_localmanagement_name" {
  description = "Database user for the management purposes"
  type        = string
}

variable "bucket_name" {
  description = "The name of the object storage bucket"
  type        = string
}