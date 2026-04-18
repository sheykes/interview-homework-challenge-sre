#
# 00-namespaces
#

resource "kubernetes_namespace" "collector" {
  metadata {
    name = "collector"
  }
}

resource "kubernetes_namespace" "integration" {
  metadata {
    name = "integration"
  }
}

resource "kubernetes_namespace" "orcrist" {
  metadata {
    name = "orcrist"
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
  }
}

resource "kubernetes_namespace" "tools" {
  metadata {
    name = "tools"
  }
}
