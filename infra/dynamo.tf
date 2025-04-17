resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = var.dynamo_table
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "identifier"

  attribute {
    name = "identifier"
    type = "S"
  }

  tags = {
    Name        = "tb_users"
    Environment = var.stage_name
  }
}