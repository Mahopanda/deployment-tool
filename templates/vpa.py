vpa_yaml_placeholder = """
---
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: {name}-vpa
  namespace: {namespace}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {name}
  updatePolicy:
    updateMode: "Auto"
"""