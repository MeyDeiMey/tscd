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

# 1. Security Group
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

  ingress {
    from_port   = 22
    to_port     = 22
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

# 2. EC2 instance
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
    git clone https://github.com/MeyDeiMey/tscd
    cd graphword-MJ

    pip3 install -r requirements.txt
    pip3 install gunicorn

    cd /home/ec2-user/graphword-MJ/app

    nohup gunicorn --bind 0.0.0.0:5001 api:app > app.log 2>&1 &
  EOF

  tags = {
    Name = "GraphWordInstance"
  }
}

# 3. API Gateway
resource "aws_apigatewayv2_api" "graph_api" {
  name          = "graph-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "http_proxy" {
  api_id            = aws_apigatewayv2_api.graph_api.id
  integration_type  = "HTTP_PROXY"
  integration_uri   = "http://${aws_instance.graph_ec2.public_dns}:5001/"
  connection_type   = "INTERNET"
  integration_method = "ANY"
}

resource "aws_apigatewayv2_route" "proxy" {
  api_id    = aws_apigatewayv2_api.graph_api.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.http_proxy.id}"
}

resource "aws_apigatewayv2_stage" "dev" {
  api_id      = aws_apigatewayv2_api.graph_api.id
  name        = "dev"
  auto_deploy = true
}

# 4. S3 Bucket
resource "aws_s3_bucket" "datamart_bucket" {
  bucket        = "graphword-datamart-bucket"
  force_destroy = true
  tags = {
    Name = "GraphWordDataMart"
  }
}

# S3 Bucket Ownership Controls
resource "aws_s3_bucket_ownership_controls" "datamart_bucket_ownership" {
  bucket = aws_s3_bucket.datamart_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# Recurso ACL para el bucket
resource "aws_s3_bucket_acl" "datamart_bucket_acl" {
  bucket = aws_s3_bucket.datamart_bucket.id
  acl    = "private"
}

# Outputs
output "api_endpoint" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}

output "ec2_public_dns" {
  value = aws_instance.graph_ec2.public_dns
}
