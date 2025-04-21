resource "aws_api_gateway_rest_api" "facial_recognition_gw_api"{
    name = "facial_recognition_api"
    description = "REST API for lambda"

    endpoint_configuration {
      types = ["REGIONAL"]
    }
}

### REGISTER ENDPOINT ###
resource "aws_api_gateway_resource" "register_gw_api_resource" {
    parent_id       = aws_api_gateway_rest_api.facial_recognition_gw_api.root_resource_id
    path_part       = "register"
    rest_api_id     = aws_api_gateway_rest_api.facial_recognition_gw_api.id
}

resource "aws_api_gateway_method" "register_gw_api_method_post" {
    authorization   = "NONE"
    http_method     = "POST"
    resource_id     = aws_api_gateway_resource.register_gw_api_resource.id
    rest_api_id     = aws_api_gateway_rest_api.facial_recognition_gw_api.id
}

resource "aws_api_gateway_integration" "register_lambda_integration_post" {
    http_method = aws_api_gateway_method.register_gw_api_method_post.http_method
    resource_id = aws_api_gateway_resource.register_gw_api_resource.id
    rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
    type        = "AWS_PROXY"

    integration_http_method     = "POST" #para lambda_proxy, sempre deve ser POST
    uri = aws_lambda_function.lambda.invoke_arn
}

resource "aws_api_gateway_method_response" "register_response_200_post" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.register_gw_api_resource.id
  http_method = aws_api_gateway_method.register_gw_api_method_post.http_method
  status_code = "200"
}

resource "aws_api_gateway_method_response" "register_response_405_post" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.register_gw_api_resource.id
  http_method = aws_api_gateway_method.register_gw_api_method_post.http_method
  status_code = "405"
}

resource "aws_api_gateway_method_response" "register_response_404_post" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.register_gw_api_resource.id
  http_method = aws_api_gateway_method.register_gw_api_method_post.http_method
  status_code = "404"
}

resource "aws_api_gateway_method" "register_options" {
  rest_api_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id   = aws_api_gateway_resource.register_gw_api_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "register_options_response" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.register_gw_api_resource.id
  http_method = aws_api_gateway_method.register_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration" "register_options_integration" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.register_gw_api_resource.id
  http_method = aws_api_gateway_method.register_options.http_method
  type        = "MOCK"
  integration_http_method = "OPTIONS"
  passthrough_behavior    = "WHEN_NO_MATCH"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_integration_response" "register_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.register_gw_api_resource.id
  http_method = aws_api_gateway_method.register_options.http_method
  status_code = aws_api_gateway_method_response.register_options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type'"
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,POST'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [aws_api_gateway_integration.register_options_integration]
}

### AUTHENTICATE ENDPOINT ###
resource "aws_api_gateway_resource" "authentication_gw_api_resource" {
    parent_id       = aws_api_gateway_rest_api.facial_recognition_gw_api.root_resource_id
    path_part       = "authentication"
    rest_api_id     = aws_api_gateway_rest_api.facial_recognition_gw_api.id
}

resource "aws_api_gateway_method" "authentication_gw_api_method_post" {
    authorization   = "NONE"
    http_method     = "POST"
    resource_id     = aws_api_gateway_resource.authentication_gw_api_resource.id
    rest_api_id     = aws_api_gateway_rest_api.facial_recognition_gw_api.id
}

resource "aws_api_gateway_integration" "authentication_lambda_integration_post" {
    http_method = aws_api_gateway_method.authentication_gw_api_method_post.http_method
    resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id
    rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
    type        = "AWS_PROXY"

    integration_http_method     = "POST" #para lambda_proxy, sempre deve ser POST
    uri = aws_lambda_function.lambda.invoke_arn
}

resource "aws_api_gateway_method_response" "authentication_response_200_post" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id #trocar
  http_method = aws_api_gateway_method.authentication_gw_api_method_post.http_method
  status_code = "200"
}

resource "aws_api_gateway_method_response" "authentication_response_405_post" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id #trocar
  http_method = aws_api_gateway_method.authentication_gw_api_method_post.http_method
  status_code = "405"
}

resource "aws_api_gateway_method_response" "authentication_response_404_post" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id #trocar
  http_method = aws_api_gateway_method.authentication_gw_api_method_post.http_method
  status_code = "404"
}

resource "aws_api_gateway_method" "authentication_options" {
  rest_api_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id   = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_method_response" "authentication_options_response" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method = aws_api_gateway_method.authentication_options.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration" "authentication_options_integration" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method = aws_api_gateway_method.authentication_options.http_method
  type        = "MOCK"
  integration_http_method = "OPTIONS"
  passthrough_behavior    = "WHEN_NO_MATCH"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_integration_response" "authentication_options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  resource_id = aws_api_gateway_resource.authentication_gw_api_resource.id
  http_method = aws_api_gateway_method.authentication_options.http_method
  status_code = aws_api_gateway_method_response.authentication_options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type'"
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS,POST,GET'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [aws_api_gateway_integration.authentication_options_integration]
}

###############

resource "aws_api_gateway_deployment" "api_deployment" {
    rest_api_id = aws_api_gateway_rest_api.facial_recognition_gw_api.id

    triggers = {
      redeployment = "${timestamp()}-${filebase64sha256("${path.module}/lambda.zip")}"
    }

    lifecycle {
      create_before_destroy = true
    }

    # 👇 Adiciona os MÉTODOS (não integrações) como dependência
    depends_on = [ 
         aws_api_gateway_integration.register_lambda_integration_post,
         aws_api_gateway_integration.authentication_lambda_integration_post
     ]
}

resource "aws_lambda_permission" "apigw_lambda_permission" {
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda.function_name
    principal = "apigateway.amazonaws.com"
    statement_id = "AllowExecutionFromAPIGateway"
    source_arn = "${aws_api_gateway_rest_api.facial_recognition_gw_api.execution_arn}/*"
}

resource "aws_api_gateway_stage" "api_stage" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.facial_recognition_gw_api.id
  stage_name    = var.stage_name
}