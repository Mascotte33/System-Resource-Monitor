output "agent_instance_1_ip" {
  description = "Public ip of agent instance 1"
  value       = aws_instance.agent_instance_1.public_ip
}
output "agent_instance_2_ip" {
  description = "Public ip of agent instance 2"
  value       = aws_instance.agent_instance_2.public_ip
}
output "observabilty_instance_ip" {
  description = "Pblic ip of the observability instance"
  value       = aws_instance.observabilty_instance.public_ip
}
