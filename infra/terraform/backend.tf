terraform {
  backend "s3" {
    bucket         = "system-monitor-bucket-kamilkolmasiak"
    key            = "system-monitor/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-lock"
  }
}
