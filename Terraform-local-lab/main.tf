terraform {
  required_version = ">= 1.0"
}

resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Hello from Terraform! This file was created at ${timestamp()}."
}

output "file_path" {
  value = local_file.hello.filename
}
