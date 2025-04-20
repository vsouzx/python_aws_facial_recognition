resource "aws_api_gateway_rest_api" "facial_recognition_gw_api" {
  name        = "facial_recognition_api"
  description = "REST API for facial recognition"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

### ===================== /register =========================
resource "aws_api_gateway_resource" "register_gw_api_resource" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  parent_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.root_resource_id
  path_part   = "register"
}

resource "aws_api_gateway_method" "register_gw_api_method_post" {
  rest_api_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id   = aws_api_gateway_resource.register_gw_api_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "register_lambda_integration_post" {
  rest_api_id             = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id             = aws_api_gateway_resource.register_gw_api_resource.id
  http_method             = aws_api_gateway_method.register_gw_api_method_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.facial_recognition_lambda.invoke_arn
}

# CORS para /register
resource "aws_api_gateway_method" "register_options" {
  rest_api_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id   = aws_api_gateway_resource.register_gw_api_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "register_options_integration" {
  rest_api_id          = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id          = aws_api_gateway_resource.register_gw_api_resource.id
  http_method          = aws_api_gateway_method.register_options.http_method
  type                 = "MOCK"
  passthrough_behavior = "WHEN_NO_MATCH"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "register_options_response" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.register_gw_api_resource.id
  http_method = aws_api_gateway_method.register_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true
  }
}

resource "aws_api_gateway_integration_response" "register_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.register_gw_api_resource.id
  http_method = aws_api_gateway_method.register_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = "'*'",
    "method.response.header.Access-Control-Allow-Headers" = "'*'",
    "method.response.header.Access-Control-Allow-Methods" = "'POST,OPTIONS'"
  }

  response_templates = {
    "application/json" = ""
  }
}

### ===================== /authentication =========================
resource "aws_api_gateway_resource" "authentication_gw_api_resource" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  parent_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.root_resource_id
  path_part   = "authentication"
}

resource "aws_api_gateway_method" "authentication_gw_api_method_post" {
  rest_api_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id   = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "authentication_lambda_integration_post" {
  rest_api_id             = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id             = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method             = aws_api_gateway_method.authentication_gw_api_method_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.facial_recognition_lambda.invoke_arn
}

# CORS para /authentication
resource "aws_api_gateway_method" "authentication_options" {
  rest_api_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id   = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "authentication_options_integration" {
  rest_api_id          = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id          = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method          = aws_api_gateway_method.authentication_options.http_method
  type                 = "MOCK"
  passthrough_behavior = "WHEN_NO_MATCH"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "authentication_options_response" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method = aws_api_gateway_method.authentication_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = true,
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true
  }
}

resource "aws_api_gateway_integration_response" "authentication_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method = aws_api_gateway_method.authentication_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"  = "'*'",
    "method.response.header.Access-Control-Allow-Headers" = "'*'",
    "method.response.header.Access-Control-Allow-Methods" = "'POST,OPTIONS'"
  }

  response_templates = {
    "application/json" = ""
  }
}

### ===================== Deploy da API =========================
resource "aws_api_gateway_deployment" "facial_recognition_gw_deployment" {
  depends_on = [
    aws_api_gateway_integration.register_lambda_integration_post,
    aws_api_gateway_integration.authentication_lambda_integration_post
  ]

  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  stage_name  = var.stage_name
}
