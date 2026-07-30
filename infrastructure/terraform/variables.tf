variable "aws_region" {

  description = "AWS Region"

  type = string

}

variable "iam_user_name" {

  description = "IAM User Name"

  type = string

}

variable "vpc_cidr" {

  description = "CIDR Block for VPC"

  type = string

}

variable "vpc_name" {

  description = "VPC Name"

  type = string

}
variable "public_subnet_cidr" {

  description = "Public Subnet CIDR"

  type = string

}

variable "availability_zone" {

  description = "Availability Zone"

  type = string

}
variable "allowed_ssh_ip" {

  description = "IP allowed to SSH"

  type = string

}
variable "instance_type" {

  type = string

}

variable "key_name" {

  type = string

}
variable "private_subnet_cidr" {

  default = "10.0.2.0/24"

}