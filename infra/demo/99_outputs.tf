output "apigw" {
  value       = "${aws_api_gateway_stage.app.invoke_url}/${var.apigw_path}"
  description = "The url of api gateway"
}
