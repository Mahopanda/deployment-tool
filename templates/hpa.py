hpa_yaml_template = """

apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: {name}-hpa
  namespace: {namespace}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {name}
  minReplicas: {min_pods}
  maxReplicas: {max_pods}
  targetCPUUtilizationPercentage: {cpu_utilization}

"""



hpa_patch_yaml_template = """

apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: {name}-hpa
spec:
  minReplicas: {min_pods}
  maxReplicas: {max_pods}
  targetCPUUtilizationPercentage: {cpu_utilization}

"""
