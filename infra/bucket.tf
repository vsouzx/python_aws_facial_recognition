resource "aws_s3_bucket" "s_facial_recognition_bucket" {
  bucket = "s-facial-recognition-bucket"
  force_destroy = true

  tags = {
    Name        = "fr-bucket"
    Environment = "prod"
  }
}

resource "aws_s3_bucket_public_access_block" "fotos_colaboradores_block" {
  bucket = aws_s3_bucket.s_facial_recognition_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}