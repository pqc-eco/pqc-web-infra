output "alb_dns_name" {
  description = "Point the domain's DNS record here"
  value       = aws_lb.this.dns_name
}

output "ecr_repository_url" {
  description = "Push the app image to this repository"
  value       = aws_ecr_repository.app.repository_url
}

output "api_url" {
  description = "Public HTTPS URL of the web API"
  value       = "https://${var.domain_name}"
}
