resource "aws_iam_role" "iam_for_lambda"{
    name                    = "iam_for_lambda"
    assume_role_policy      = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "lambda_logging" {
    name = "lambda_logging"
    path = "/"
    description = "IAM policy for logging from a lambda"

    policy = <<EOF
    {
        "Version":"2012-10-17",
        "Statement": [
            {
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*",
                "Effect": "Allow"
            },
            {
                "Action": [
                    "dynamodb:*"
                ],
                "Resource": "*",
                "Effect": "Allow"
            },
            {
                "Action": [
                    "s3:*"
                ],
                "Resource": "arn:aws:s3:::s-facial-recognition-bucket/*",
                "Effect": "Allow"
            },
            {
                "Action": [
                    "rekognition:*"
                ],
                "Resource": "*",
                "Effect": "Allow"
            }
        ]
    }
    EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
    role = aws_iam_role.iam_for_lambda.name
    policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_lambda_function" "lambda" {
  function_name    = "facial_recognition_lambda"
  role             = aws_iam_role.iam_for_lambda.arn
  runtime          = "python3.10"
  handler          = "lambda.lambda_handler"
  filename         = "lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")

  environment {
    variables = {
      API_GATEWAY_URL = var.api_gateway_url
      DYNAMODB_TABLE  = var.dynamo_table
      BUCKET_NAME = var.bucket_name
      COLLECTION_ID = var.collection_id
    }
  }
}

resource "aws_cloudwatch_log_group" "example"{
    name = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
    retention_in_days = var.log_retention_days
}