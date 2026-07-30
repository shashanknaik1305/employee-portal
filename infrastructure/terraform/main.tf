data "aws_ami" "ubuntu" {

  most_recent = true

  owners = ["099720109477"]

  filter {
    name = "name"

    values = [
      "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
    ]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

########################################
# IAM USER (Demo)
########################################

resource "aws_iam_user" "demo_user" {

  name = var.iam_user_name

}

########################################
# IAM ROLE FOR EC2
########################################

resource "aws_iam_role" "ec2_role" {

  name = "employee-portal-ec2-role"

  assume_role_policy = jsonencode({

    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

########################################
# ATTACH ECR READONLY POLICY
########################################

resource "aws_iam_role_policy_attachment" "ecr_readonly" {

  role = aws_iam_role.ec2_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"

}

########################################
# INSTANCE PROFILE
########################################

resource "aws_iam_instance_profile" "ec2_profile" {

  name = "employee-portal-instance-profile"

  role = aws_iam_role.ec2_role.name

}

########################################
# VPC
########################################

resource "aws_vpc" "main" {

  cidr_block = var.vpc_cidr

  enable_dns_support = true

  enable_dns_hostnames = true

  tags = {
    Name = var.vpc_name
  }
}

########################################
# PUBLIC SUBNET
########################################

resource "aws_subnet" "public_subnet" {

  vpc_id = aws_vpc.main.id

  cidr_block = var.public_subnet_cidr

  availability_zone = var.availability_zone

  map_public_ip_on_launch = true

  tags = {
    Name = "employee-portal-public-subnet"
  }
}

########################################
# INTERNET GATEWAY
########################################

resource "aws_internet_gateway" "igw" {

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "employee-portal-igw"
  }
}

########################################
# ROUTE TABLE
########################################

resource "aws_route_table" "public_rt" {

  vpc_id = aws_vpc.main.id

  route {

    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "employee-portal-public-rt"
  }
}

########################################
# ROUTE TABLE ASSOCIATION
########################################

resource "aws_route_table_association" "public_assoc" {

  subnet_id = aws_subnet.public_subnet.id

  route_table_id = aws_route_table.public_rt.id

}

########################################
# SECURITY GROUP
########################################

resource "aws_security_group" "employee_sg" {

  name = "employee-portal-sg"

  description = "Security Group for Employee Portal"

  vpc_id = aws_vpc.main.id

  ingress {

    description = "SSH"

    from_port = 22

    to_port = 22

    protocol = "tcp"

    cidr_blocks = [
      var.allowed_ssh_ip
    ]
  }

  ingress {

    description = "HTTP"

    from_port = 80

    to_port = 80

    protocol = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  egress {

    from_port = 0

    to_port = 0

    protocol = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {

    Name = "employee-portal-sg"

  }
}

########################################
# EC2 INSTANCE
########################################

resource "aws_instance" "employee_server" {

  ami = data.aws_ami.ubuntu.id

  instance_type = var.instance_type

  subnet_id = aws_subnet.public_subnet.id

  vpc_security_group_ids = [
    aws_security_group.employee_sg.id
  ]

  key_name = var.key_name

  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  tags = {

    Name = "employee-portal-server"

  }
}

resource "aws_subnet" "private_subnet" {

  vpc_id = aws_vpc.main.id

  cidr_block = var.private_subnet_cidr

  availability_zone = var.availability_zone

  map_public_ip_on_launch = false

  tags = {
    Name = "employee-portal-private-subnet"
  }
}
