variable "aws_region" {
  description = "AWS region to deploy"
  type        = string
  default     = "eu-central-1"
}

variable "instance_type" {
  description = "AWS VM type"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI ID for EC2 VMs "
  type        = string
  default     = "ami-051eaec1417c5d4ae"
}

variable "key_name" {
  description = "EC2 key pair name"
  type        = string
}
