output "iam_user_name" {

  value = aws_iam_user.demo_user.name

}

output "iam_user_arn" {

  value = aws_iam_user.demo_user.arn

}
output "vpc_id" {

  value = aws_vpc.main.id

}
output "public_subnet_id" {

  value = aws_subnet.public_subnet.id

}
output "internet_gateway_id" {

  value = aws_internet_gateway.igw.id

}

output "route_table_id" {

  value = aws_route_table.public_rt.id

}
output "security_group_id" {

  value = aws_security_group.employee_sg.id

}
output "ec2_public_ip" {

  value = aws_instance.employee_server.public_ip

}

output "ec2_instance_id" {

  value = aws_instance.employee_server.id

}
output "private_subnet_id" {

  value = aws_subnet.private_subnet.id

}