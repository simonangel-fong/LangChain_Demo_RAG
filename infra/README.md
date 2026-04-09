```sh
terraform -chdir=infra init -backend-config=backend.config -reconfigure
terraform -chdir=infra fmt && terraform -chdir=infra validate
terraform -chdir=infra apply -auto-approve
```
