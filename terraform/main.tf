# ECR Repository
resource "aws_ecr_repository" "sentiment_api" {
  name                 = "sentiment-api"
  image_tag_mutability = "MUTABLE"
  force_delete         = true   # makes cleanup easy

  image_scanning_configuration {
    scan_on_push = true
  }
}

# VPC for the EKS cluster
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name = "sentiment-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = true   # cheaper, only one NAT gateway
  enable_dns_hostnames   = true
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Enable Kubernetes API access from your machine (for kubectl)
  cluster_endpoint_public_access = true

  # IAM role for the service account (IRSA) so pods can pull from ECR
  enable_irsa = true

  eks_managed_node_groups = {
    main = {
      desired_size = var.desired_capacity
      max_size     = 3
      min_size     = 1

      instance_types = [var.node_instance_type]

      labels = {
        Environment = "prod"
      }

      additional_tags = {
        Name = "sentiment-api-node"
      }
    }
  }
}

# Kubernetes provider configuration (so we can optionally apply k8s resources with Terraform)
data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_name
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}