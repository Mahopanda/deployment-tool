secret_template = """
---
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: {name}
  namespace: {namespace}
data:
{data}
"""