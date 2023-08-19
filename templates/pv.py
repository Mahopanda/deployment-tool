# accessModes: 這指定了PV可以如何被access。常見的模式有：

# ReadWriteOnce (RWO): 可以被單個node進行read-write。
# ReadOnlyMany (ROX): 可以被多個node進行read-only。
# ReadWriteMany (RWX): 可以被多個node進行read-write。
# persistentVolumeReclaimPolicy: 這指定了當PVC被刪除時，PV應該如何處理。它可以是以下其中之一：

# Retain: 保留數據，但PV不會被自動回收和重用。
# Delete: PV和相關的存儲會被自動刪除。
# Recycle: 舊數據會被刪除，然後PV可以被重新使用。
# storageClassName: 如果PV使用了存儲類 (StorageClass) 進行動態供應，這將指定存儲類的名稱。

# volumeMode: 可以是 Filesystem（默認）或 Block。大多數情況下，你會使用Filesystem。

# capacity: 指定PV的容量。

# hostPath: 對於單節點的開發或測試環境，可以使用hostPath。它將文件或目錄從主機的文件系統掛載到Pod中。

# gcePersistentDisk: 如果在GCP上，你會使用這個選項來指定GCE磁盤的相關設置。


pv_yaml_template = """
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: {pv_name}
spec:
  storageClassName: {storage_class}
  capacity:
    storage: {size}
  accessModes:
    - {access_mode}
  persistentVolumeReclaimPolicy: Retain
  volumeMode: Filesystem
  # 如果在GCP上並且使用GCE磁盤，你會使用以下設置：
  gcePersistentDisk:
    pdName: {gce_disk_name}
    fsType: ext4
  # 對於開發或測試，你可能會使用hostPath，但這在生產環境中是不推薦的：
  # hostPath:
  #   path: {path_on_host}
  #   type: DirectoryOrCreate
"""
