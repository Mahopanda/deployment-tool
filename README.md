## Kubernetes YAML Generator

這是一個用於通過問答方式生成 Kubernetes 的 YAML 配置的工具。

## 前提條件

- 請確保系統中已安裝了 `kustomize` 和 `kubectl`。
- 這只是一個範本，請根據您的具體需求進行調整。

## 使用方法

### 1. 生成 YAML 配置

運行以下 Python 腳本以生成 YAML 配置：


### 1. 生成 YAML 配置

運行以下 Python 腳本以生成 YAML 配置：

```bash
python generate_yaml.py -o /path/to/output/directory
```
在生成結束後，你將在指定目錄中看到一組基於你的輸入生成的 YAML 文件。

### 2. Dry-run 模式
在執行 deploy.sh 時，你可以使用 dry-run 選項來檢查產生的 YAML 內容，而不真的進行部署：
```bash
./deploy.sh dev --dry-run
```

## 注意事項
尚未使用kusomize，請自行測試。
尚未在kubernetes上測試，請自行測試。

在進行部署之前，建議首先使用 dry-run 選項進行檢查，確保一切正常。



### 3. 部署到 Kubernetes

首先，賦予 `deploy.sh` 執行權限：

```bash
chmod +x deploy.sh
```

接著，使用以下指令部署到指定的環境：

- 部署到開發環境：

  ```bash
  ./deploy.sh dev
  ```

- 部署到測試環境：

  ```bash
  ./deploy.sh stage
  ```

- 部署到生產環境：

  ```bash
  ./deploy.sh prod
  ```
