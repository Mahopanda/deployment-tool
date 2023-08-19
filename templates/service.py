service_yaml_template = """
apiVersion: v1
kind: Service
metadata:
  name: {name}
  namespace: {namespace}
spec:
  selector:
    app: {name}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
"""