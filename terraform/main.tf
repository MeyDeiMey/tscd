provider "aws" {
  region     = "us-east-1"
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
  token      = var.aws_session_token
}

variable "aws_access_key_id" {}
variable "aws_secret_access_key" {}
variable "aws_session_token" {}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "graph_sg" {
  name        = "graph_sg"
  description = "Allow inbound on port 5001"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5001
    to_port     = 5001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "graph_ec2" {
  ami           = "ami-0e731c8a588258d0d"
  instance_type = "t2.micro"
  subnet_id     = tolist(data.aws_subnets.default.ids)[0]
  vpc_security_group_ids = [aws_security_group.graph_sg.id]
  associate_public_ip_address = true
  user_data = <<-EOF
    #!/bin/bash
    dnf update -y
    dnf install -y python3-pip git
    cd /home/ec2-user
    git clone https://github.com/JoaquinIP/graphword-mj
    cd graphword-mj
    pip3 install -r requirements.txt
    nohup python3 api/api.py > api.log 2>&1 &
  EOF

  tags = {
    Name = "GraphWordInstance"
  }
}

resource "aws_s3_bucket" "datamart_bucket" {
  bucket = "graphword-datamart-bucket"
  acl    = "private"
  tags = {
    Name = "GraphWordDataMart"
  }
}

resource "aws_dynamodb_table" "graph_table" {
  name         = "GraphNodes"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "node"

  attribute {
    name = "node"
    type = "S"
  }

  attribute {
    name = "connected_nodes"
    type = "S"
  }

  tags = {
    Name = "GraphNodesTable"
  }
}
