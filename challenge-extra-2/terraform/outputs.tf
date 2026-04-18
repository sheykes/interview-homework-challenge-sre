output "namespaces" {
  description = "Created namespaces"
  value = [
    kubernetes_namespace.collector.metadata[0].name,
    kubernetes_namespace.integration.metadata[0].name,
    kubernetes_namespace.orcrist.metadata[0].name,
    kubernetes_namespace.monitoring.metadata[0].name,
    kubernetes_namespace.tools.metadata[0].name,
  ]
}

output "nginx_deployment" {
  description = "nginx deployment name and namespace"
  value = {
    name      = kubernetes_deployment.nginx.metadata[0].name
    namespace = kubernetes_deployment.nginx.metadata[0].namespace
    replicas  = kubernetes_deployment.nginx.spec[0].replicas
  }
}

output "nginx_service" {
  description = "nginx service name and namespace"
  value = {
    name      = kubernetes_service.nginx.metadata[0].name
    namespace = kubernetes_service.nginx.metadata[0].namespace
  }
}

output "pods" {
  description = "Created pods"
  value = {
    pod-example-orcrist    = kubernetes_pod.example_orcrist.metadata[0].name
    pod-nginx-tools        = kubernetes_pod.nginx_tools.metadata[0].name
    pod-example-integration = kubernetes_pod.example_integration.metadata[0].name
    pod-example-monitoring  = kubernetes_pod.example_monitoring.metadata[0].name
  }
}
