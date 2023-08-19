# accessModes: 和PV的 accessModes 一樣，這指定了PVC可以如何被 access。常見的模式有：

# ReadWriteOnce (RWO)
# ReadOnlyMany (ROX)
# ReadWriteMany (RWX)
# storageClassName: 如果PVC需要使用特定的 StorageClass，則此選項用於指定它。

# resources: 用於指定PVC所需的存儲量。

# selector: 允許你指定一組標籤，用於選擇一個特定的PV。

# volumeName: 允許你指定一個特定的PV的名稱，這通常在你想綁定到一個特定的PV時使用。

pvc_yaml_template = """
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {pvc_name}
spec:
  storageClassName: {storage_class}
  accessModes:
    - {access_mode}
  resources:
    requests:
      storage: {size}
  # 選擇特定的PV（通常情況下你不需要這個，除非你有特定的需求）:
  # volumeName: {specific_pv_name}
  # 使用標籤選擇器選擇PV:
  # selector:
  #   matchLabels:
  #     key1: value1
  #     key2: value2
"""