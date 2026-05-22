provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "agent_sg" {
  name        = "agent_sg"
  description = "Security group for monitor agent VMs"

  ingress {
    description = "Prometheus scrape"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Outbound all"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_security_group" "observability_sg" {
  name        = "observability_sg"
  description = "Security group for observabilty"

  ingress {
    description = "Prometheus UI"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Grafana UI"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    description = "Outbound all"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "agent_instance_1" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.agent_sg.id]
  user_data              = file("${path.module}/scripts/agent_user_data.sh")
  tags = {
    Name = "monitor-agent-1"
  }
}

resource "aws_instance" "agent_instance_2" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.agent_sg.id]
  user_data              = file("${path.module}/scripts/agent_user_data.sh")
  tags = {
    Name = "monitor-agent-2"
  }
}

resource "aws_instance" "observabilty_instance" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.observability_sg.id]
  tags = {
    Name = "observabilty_instance"
  }
}
