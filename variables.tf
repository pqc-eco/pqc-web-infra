variable "region" {
  type    = string
  default = "us-east-1"
}

variable "name" {
  type    = string
  default = "pqc-web"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "image_uri" {
  description = "Container image URI including tag, for example <account>.dkr.ecr.<region>.amazonaws.com/pqc-web:1.0.0"
  type        = string
}

variable "certificate_arn" {
  description = "ACM certificate ARN for the HTTPS listener"
  type        = string
}

variable "jwt_private_key_secret_arn" {
  description = "Secrets Manager ARN holding the JWT private key PEM"
  type        = string
}

variable "data_key_secret_arn" {
  description = "Secrets Manager ARN holding the base64 32-byte data encryption key"
  type        = string
}

variable "database_url_secret_arn" {
  description = "Secrets Manager ARN holding the DATABASE_URL"
  type        = string
}

variable "container_port" {
  type    = number
  default = 8080
}

variable "cpu" {
  type    = number
  default = 256
}

variable "memory" {
  type    = number
  default = 512
}

variable "desired_count" {
  type    = number
  default = 2
}
