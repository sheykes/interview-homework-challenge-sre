# Terraform instead of kubectl

For this task I had to take the manifest YAML files and convert them into
terraform configuration. As terraform builds a full state it is not necessary
to give the configuration files numbers, terraform builds it in a way that fits
together and takes dependencies into consideration, unlike kubectl which just
applies one after another.

## Project Structure

Each Terraform file maps 1:1 to one of the original YAML files, keeping the same
logical separation — namespaces, deployments, and pods are each defined in their own file.

Provider configuration and the `kube_context` variable live in `main.tf` and `variables.tf`,
letting you target different clusters without touching the resource definitions.

---

## Implicit Dependencies

Rather than hardcoding namespace names as strings, resources reference the namespace
Terraform object directly (e.g. `kubernetes_namespace.orcrist.metadata[0].name`).
This creates **implicit dependencies** in the graph, so Terraform always provisions
namespaces before the workloads that live inside them — no `depends_on` needed.

---

## Usage

This assumes minikube to be the kubernetes provider.

```bash
# Initialize the provider
terraform init

# Preview changes
terraform plan -var="kube_context=minikube"

# Apply
terraform apply

# Tear down
terraform destroy
```

This is what was applied on my test system:

```
stefan@fedora:~/Dokumente/orcrist/interview-homework-challenge-sre/challenge-extra-2/terraform$ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # kubernetes_deployment.nginx will be created
  + resource "kubernetes_deployment" "nginx" {
      + id               = (known after apply)
      + wait_for_rollout = true

      + metadata {
          + generation       = (known after apply)
          + labels           = {
              + "app" = "nginx"
            }
          + name             = "nginx-deployment"
          + namespace        = "orcrist"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }

      + spec {
          + min_ready_seconds         = 0
          + paused                    = false
          + progress_deadline_seconds = 600
          + replicas                  = "3"
          + revision_history_limit    = 10

          + selector {
              + match_labels = {
                  + "app" = "nginx"
                }
            }

          + strategy (known after apply)

          + template {
              + metadata {
                  + generation       = (known after apply)
                  + labels           = {
                      + "app" = "nginx"
                    }
                  + name             = (known after apply)
                  + resource_version = (known after apply)
                  + uid              = (known after apply)
                }
              + spec {
                  + automount_service_account_token  = true
                  + dns_policy                       = "ClusterFirst"
                  + enable_service_links             = true
                  + host_ipc                         = false
                  + host_network                     = false
                  + host_pid                         = false
                  + hostname                         = (known after apply)
                  + node_name                        = (known after apply)
                  + restart_policy                   = "Always"
                  + scheduler_name                   = (known after apply)
                  + service_account_name             = (known after apply)
                  + share_process_namespace          = false
                  + termination_grace_period_seconds = 30

                  + container {
                      + image                      = "nginx:latest"
                      + image_pull_policy          = (known after apply)
                      + name                       = "nginx"
                      + stdin                      = false
                      + stdin_once                 = false
                      + termination_message_path   = "/dev/termination-log"
                      + termination_message_policy = (known after apply)
                      + tty                        = false

                      + port {
                          + container_port = 80
                          + protocol       = "TCP"
                        }

                      + resources (known after apply)
                    }

                  + image_pull_secrets (known after apply)

                  + readiness_gate (known after apply)
                }
            }
        }
    }

  # kubernetes_namespace.collector will be created
  + resource "kubernetes_namespace" "collector" {
      + id                               = (known after apply)
      + wait_for_default_service_account = false

      + metadata {
          + generation       = (known after apply)
          + name             = "collector"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }
    }

  # kubernetes_namespace.integration will be created
  + resource "kubernetes_namespace" "integration" {
      + id                               = (known after apply)
      + wait_for_default_service_account = false

      + metadata {
          + generation       = (known after apply)
          + name             = "integration"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }
    }

  # kubernetes_namespace.monitoring will be created
  + resource "kubernetes_namespace" "monitoring" {
      + id                               = (known after apply)
      + wait_for_default_service_account = false

      + metadata {
          + generation       = (known after apply)
          + name             = "monitoring"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }
    }

  # kubernetes_namespace.orcrist will be created
  + resource "kubernetes_namespace" "orcrist" {
      + id                               = (known after apply)
      + wait_for_default_service_account = false

      + metadata {
          + generation       = (known after apply)
          + name             = "orcrist"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }
    }

  # kubernetes_namespace.tools will be created
  + resource "kubernetes_namespace" "tools" {
      + id                               = (known after apply)
      + wait_for_default_service_account = false

      + metadata {
          + generation       = (known after apply)
          + name             = "tools"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }
    }

  # kubernetes_pod.example_integration will be created
  + resource "kubernetes_pod" "example_integration" {
      + id = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "pod-example-integration"
          + namespace        = "integration"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }

      + spec {
          + automount_service_account_token  = true
          + dns_policy                       = "ClusterFirst"
          + enable_service_links             = true
          + host_ipc                         = false
          + host_network                     = false
          + host_pid                         = false
          + hostname                         = (known after apply)
          + node_name                        = (known after apply)
          + restart_policy                   = "Always"
          + scheduler_name                   = (known after apply)
          + service_account_name             = (known after apply)
          + share_process_namespace          = false
          + termination_grace_period_seconds = 30

          + container {
              + args                       = [
                  + "cat",
                ]
              + image                      = "alpine"
              + image_pull_policy          = (known after apply)
              + name                       = "pod"
              + stdin                      = true
              + stdin_once                 = false
              + termination_message_path   = "/dev/termination-log"
              + termination_message_policy = (known after apply)
              + tty                        = true

              + resources (known after apply)
            }

          + image_pull_secrets (known after apply)

          + readiness_gate (known after apply)
        }
    }

  # kubernetes_pod.example_monitoring will be created
  + resource "kubernetes_pod" "example_monitoring" {
      + id = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "pod-example-monitoring"
          + namespace        = "monitoring"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }

      + spec {
          + automount_service_account_token  = true
          + dns_policy                       = "ClusterFirst"
          + enable_service_links             = true
          + host_ipc                         = false
          + host_network                     = false
          + host_pid                         = false
          + hostname                         = (known after apply)
          + node_name                        = (known after apply)
          + restart_policy                   = "Always"
          + scheduler_name                   = (known after apply)
          + service_account_name             = (known after apply)
          + share_process_namespace          = false
          + termination_grace_period_seconds = 30

          + container {
              + args                       = [
                  + "cat",
                ]
              + image                      = "alpine"
              + image_pull_policy          = (known after apply)
              + name                       = "pod"
              + stdin                      = true
              + stdin_once                 = false
              + termination_message_path   = "/dev/termination-log"
              + termination_message_policy = (known after apply)
              + tty                        = true

              + resources (known after apply)
            }

          + image_pull_secrets (known after apply)

          + readiness_gate (known after apply)
        }
    }

  # kubernetes_pod.example_orcrist will be created
  + resource "kubernetes_pod" "example_orcrist" {
      + id = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "pod-example-orcrist"
          + namespace        = "orcrist"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }

      + spec {
          + automount_service_account_token  = true
          + dns_policy                       = "ClusterFirst"
          + enable_service_links             = true
          + host_ipc                         = false
          + host_network                     = false
          + host_pid                         = false
          + hostname                         = (known after apply)
          + node_name                        = (known after apply)
          + restart_policy                   = "Always"
          + scheduler_name                   = (known after apply)
          + service_account_name             = (known after apply)
          + share_process_namespace          = false
          + termination_grace_period_seconds = 30

          + container {
              + args                       = [
                  + "cat",
                ]
              + image                      = "alpine"
              + image_pull_policy          = (known after apply)
              + name                       = "pod"
              + stdin                      = true
              + stdin_once                 = false
              + termination_message_path   = "/dev/termination-log"
              + termination_message_policy = (known after apply)
              + tty                        = true

              + resources (known after apply)
            }

          + image_pull_secrets (known after apply)

          + readiness_gate (known after apply)
        }
    }

  # kubernetes_pod.nginx_tools will be created
  + resource "kubernetes_pod" "nginx_tools" {
      + id = (known after apply)

      + metadata {
          + generation       = (known after apply)
          + name             = "pod-nginx-tools"
          + namespace        = "tools"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }

      + spec {
          + automount_service_account_token  = true
          + dns_policy                       = "ClusterFirst"
          + enable_service_links             = true
          + host_ipc                         = false
          + host_network                     = false
          + host_pid                         = false
          + hostname                         = (known after apply)
          + node_name                        = (known after apply)
          + restart_policy                   = "Always"
          + scheduler_name                   = (known after apply)
          + service_account_name             = (known after apply)
          + share_process_namespace          = false
          + termination_grace_period_seconds = 30

          + container {
              + image                      = "nginx"
              + image_pull_policy          = (known after apply)
              + name                       = "pod"
              + stdin                      = false
              + stdin_once                 = false
              + termination_message_path   = "/dev/termination-log"
              + termination_message_policy = (known after apply)
              + tty                        = false

              + port {
                  + container_port = 80
                  + name           = "web"
                  + protocol       = "TCP"
                }

              + resources (known after apply)
            }

          + image_pull_secrets (known after apply)

          + readiness_gate (known after apply)
        }
    }

  # kubernetes_service.nginx will be created
  + resource "kubernetes_service" "nginx" {
      + id                     = (known after apply)
      + status                 = (known after apply)
      + wait_for_load_balancer = true

      + metadata {
          + generation       = (known after apply)
          + name             = "nginx-service"
          + namespace        = "orcrist"
          + resource_version = (known after apply)
          + uid              = (known after apply)
        }

      + spec {
          + allocate_load_balancer_node_ports = true
          + cluster_ip                        = (known after apply)
          + cluster_ips                       = (known after apply)
          + external_traffic_policy           = (known after apply)
          + health_check_node_port            = (known after apply)
          + internal_traffic_policy           = (known after apply)
          + ip_families                       = (known after apply)
          + ip_family_policy                  = (known after apply)
          + publish_not_ready_addresses       = false
          + selector                          = {
              + "app" = "nginx"
            }
          + session_affinity                  = "None"
          + type                              = "ClusterIP"

          + port {
              + node_port   = (known after apply)
              + port        = 80
              + protocol    = "TCP"
              + target_port = "80"
            }

          + session_affinity_config (known after apply)
        }
    }

Plan: 11 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

kubernetes_namespace.collector: Creating...
kubernetes_namespace.monitoring: Creating...
kubernetes_namespace.tools: Creating...
kubernetes_namespace.orcrist: Creating...
kubernetes_namespace.integration: Creating...
kubernetes_namespace.tools: Creation complete after 0s [id=tools]
kubernetes_namespace.collector: Creation complete after 0s [id=collector]
kubernetes_namespace.integration: Creation complete after 0s [id=integration]
kubernetes_pod.nginx_tools: Creating...
kubernetes_namespace.monitoring: Creation complete after 0s [id=monitoring]
kubernetes_namespace.orcrist: Creation complete after 0s [id=orcrist]
kubernetes_service.nginx: Creating...
kubernetes_pod.example_integration: Creating...
kubernetes_pod.example_orcrist: Creating...
kubernetes_pod.example_monitoring: Creating...
kubernetes_deployment.nginx: Creating...
kubernetes_service.nginx: Creation complete after 0s [id=orcrist/nginx-service]
kubernetes_pod.nginx_tools: Still creating... [00m10s elapsed]
kubernetes_pod.example_orcrist: Still creating... [00m10s elapsed]
kubernetes_pod.example_monitoring: Still creating... [00m10s elapsed]
kubernetes_pod.example_integration: Still creating... [00m10s elapsed]
kubernetes_deployment.nginx: Still creating... [00m10s elapsed]
kubernetes_pod.nginx_tools: Creation complete after 13s [id=tools/pod-nginx-tools]
kubernetes_pod.example_orcrist: Still creating... [00m20s elapsed]
kubernetes_pod.example_integration: Still creating... [00m20s elapsed]
kubernetes_pod.example_monitoring: Still creating... [00m20s elapsed]
kubernetes_deployment.nginx: Still creating... [00m20s elapsed]
kubernetes_pod.example_integration: Creation complete after 23s [id=integration/pod-example-integration]
kubernetes_pod.example_orcrist: Creation complete after 23s [id=orcrist/pod-example-orcrist]
kubernetes_pod.example_monitoring: Creation complete after 23s [id=monitoring/pod-example-monitoring]
kubernetes_deployment.nginx: Creation complete after 26s [id=orcrist/nginx-deployment]

Apply complete! Resources: 11 added, 0 changed, 0 destroyed.

Outputs:

namespaces = [
  "collector",
  "integration",
  "orcrist",
  "monitoring",
  "tools",
]
nginx_deployment = {
  "name" = "nginx-deployment"
  "namespace" = "orcrist"
  "replicas" = "3"
}
nginx_service = {
  "name" = "nginx-service"
  "namespace" = "orcrist"
}
pods = {
  "pod-example-integration" = "pod-example-integration"
  "pod-example-monitoring" = "pod-example-monitoring"
  "pod-example-orcrist" = "pod-example-orcrist"
  "pod-nginx-tools" = "pod-nginx-tools"
}
```
