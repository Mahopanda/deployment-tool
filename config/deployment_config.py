import re

class DeploymentConfig:
    def __init__(self):
        self.name = ""
        self.image = ""
        self.replicas = 0
        self.namespace = ""
        self.hpa = None
        self.vpa = False
        self.environments = {}
        self.configmaps = {}
        self.secrets = {}
        self.deploy_environments = []
        self.pv = None 
        self.pvc = None  
        self.service = None
        self.cpu_request = ""
        self.memory_request = ""
        self.cpu_limit = ""
        self.memory_limit = ""
        self.deploy_environments = []

    def get_input(self, prompt, validation_func=None, allow_empty=False):
        while True:
            value = input(prompt).strip()
            if not value:
                if allow_empty:
                    return None
                else:
                    print("這是必填項，請重新輸入。")
                    continue
            if not validation_func or validation_func(value):
                return value
            print("無效的輸入，請重新輸入。")


    def validate_name_format(self, name: str) -> bool:
        if "_" in name:
            print("名稱不能包含 '_', 請使用 '-' 代替。")
            return False
        return True
    
    def validate_cpu_input(self, value: str) -> bool:
        # 檢查是否為有效的 CPU 值，例如 100m 或 1
        return bool(re.match(r'^(\d+m|\d+(\.\d{1,2})?)$', value))

    def validate_memory_input(self, value: str) -> bool:
        # 檢查是否為有效的記憶體值，例如 256Mi 或 1Gi
        return bool(re.match(r'^\d+(Mi|Gi|Ki)?$', value))


    def ask_basic_questions(self):
        self.name = self.get_input("請輸入 Deployment 的名稱: ", validation_func=self.validate_name_format, allow_empty=False)
        self.image = self.get_input("請輸入 Docker 映像檔的名稱: ", allow_empty=False)
        self.replicas = int(self.get_input("請輸入 Pod 的副本數量 (例如: 3): ", validation_func=lambda x: x.isdigit()))
        self.namespace = self.get_input("請輸入 namespace (預設值: default): ", allow_empty=True) or "default"
        self.ask_environments()


    def ask_environment_specific_questions(self, env):
        print(f"\n配置 {env} 環境:")
        cpu_request = self.get_input(f"{env} 環境: 請輸入 CPU 的請求數值 (例如: 100m): ", validation_func=self.validate_cpu_input)
        memory_request = self.get_input(f"{env} 環境: 請輸入記憶體的請求數值 (例如: 256Mi): ", validation_func=self.validate_memory_input)
        cpu_limit = self.get_input(f"{env} 環境: 請輸入 CPU 的限制數值 (例如: 1): ", validation_func=self.validate_cpu_input)
        memory_limit = self.get_input(f"{env} 環境: 請輸入記憶體的限制數值 (例如: 512Mi): ", validation_func=self.validate_memory_input)
        
        self.environments[env] = {
            "cpuRequest": cpu_request,
            "memoryRequest": memory_request,
            "cpuLimit": cpu_limit,
            "memoryLimit": memory_limit
        }

    def ask_environments(self):
        available_environments = ["dev", "stage", "prod"]
        print("請選擇您希望配置的環境 (輸入 'done' 結束選擇):")
        for env in available_environments:
            choice = self.get_input(f"是否要開啟 {env} 環境? (yes/no): ", validation_func=lambda x: x in ["yes", "no"])
            if choice == "yes":
                self.deploy_environments.append(env)
                self.ask_environment_specific_questions(env)

    def ask_environment_specific_questions(self, env):
        print(f"\n配置 {env} 環境:")
        # Here, ask the specific questions for the environment
        # For example:
        self.environments[env] = {
            "cpuRequest": self.get_input(f"{env} 環境: 請輸入 CPU 的請求數值 (例如: 100m): "),
            "memoryRequest": self.get_input(f"{env} 環境: 請輸入記憶體的請求數值 (例如: 256Mi): "),
            "cpuLimit": self.get_input(f"{env} 環境: 請輸入 CPU 的限制數值 (例如: 1): "),
            "memoryLimit": self.get_input(f"{env} 環境: 請輸入記憶體的限制數值 (例如: 512Mi): ")
        }


    def ask_configmap_questions(self):
        configmap_choice = self.get_input("是否要添加 ConfigMap? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
        while configmap_choice == "yes":
            configmap_name = self.get_input("請輸入 ConfigMap 的名稱: ")
            self.configmaps[configmap_name] = {}
            key = self.get_input("請輸入 ConfigMap 中的 key (輸入 'exit' 退出): ", allow_empty=True)
            while key != "exit":
                value = self.get_input(f"請為 key '{key}' 輸入 value: ")
                self.configmaps[configmap_name][key] = value
                key = self.get_input("請輸入 ConfigMap 中的 key (輸入 'exit' 退出): ", allow_empty=True)
            configmap_choice = self.get_input("是否要繼續添加 ConfigMap? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])


    def ask_secret_questions(self):
        secret_choice = self.get_input("是否要添加 Secret? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
        while secret_choice == "yes":
            secret_name = self.get_input("請輸入 Secret 的名稱: ", allow_empty=False)
            self.secrets[secret_name] = {}
            key = self.get_input("請輸入 Secret 中的 key (輸入 'exit' 退出): ", allow_empty=True)
            while key != "exit":
                value = self.get_input(f"請為 key '{key}' 輸入 value: ", allow_empty=False)
                self.secrets[secret_name][key] = value
                key = self.get_input("請輸入 Secret 中的 key (輸入 'exit' 退出): ", allow_empty=True)
            secret_choice = self.get_input("是否要繼續添加 Secret? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])

    def ask_hpa_questions(self):
        hpa_choice = self.get_input("是否要添加 HPA? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
        if hpa_choice == "yes":
            min_pods = int(self.get_input("請輸入最小的 Pod 數量: ", validation_func=lambda x: x.isdigit()))
            max_pods = int(self.get_input("請輸入最大的 Pod 數量: ", validation_func=lambda x: x.isdigit()))
            cpu_utilization = int(self.get_input("請輸入CPU使用率的目標百分比 (例如: 80): ", validation_func=lambda x: x.isdigit()))
            self.hpa = {
                "minPods": min_pods,
                "maxPods": max_pods,
                "cpuUtilization": cpu_utilization
            }

    def ask_vpa_questions(self):
        vpa_choice = self.get_input("是否要添加 VPA? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
        self.vpa = True if vpa_choice == "yes" else False

    def ask_environment_questions(self):
        env_choice = self.get_input("是否要添加環境變數? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
        while env_choice == "yes":
            key = self.get_input("請輸入環境變數的名稱 (輸入 'exit' 退出): ", allow_empty=True)
            if key == "exit":
                break
            value = self.get_input(f"請為變數 '{key}' 輸入值: ")
            self.environments[key] = value
            env_choice = self.get_input("是否要繼續添加環境變數? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])

    def ask_environments_to_deploy(self):
        environments = ["dev", "stage", "prod"]
        chosen_envs = []
        
        print("請選擇要部署的環境 (可以選擇多個):")
        for idx, env in enumerate(environments, 1):
            choice = self.get_input(f"{idx}. 是否要部署到 {env}? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
            if choice == "yes":
                chosen_envs.append(env)
        
        self.deploy_environments = chosen_envs

    def ask_storage_questions(self):
        pv_choice = self.get_input("是否要添加 Persistent Volume (PV)? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
        if pv_choice == "yes":
            size = self.get_input("請輸入 PV 的大小 (例如: 10Gi): ")
            storage_class_choice = self.get_input("請選擇 StorageClass (1: standard, 2: premium, 3: 自定義): ", validation_func=lambda x: x in ['1', '2', '3'])
            if storage_class_choice == '1':
                storage_class = 'standard'
            elif storage_class_choice == '2':
                storage_class = 'premium'
            else:
                storage_class = self.get_input("請輸入自定義的 StorageClass 名稱: ", allow_empty=False)

            self.pv = {
                "size": size,
                "storageClass": storage_class or None
            }

            pvc_choice = self.get_input("是否要添加 Persistent Volume Claim (PVC)? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
            if pvc_choice == "yes":
                access_modes = self.get_input("請輸入 PVC 的存取模式 (例如: ReadWriteOnce): ")
                self.pvc = {
                    "accessModes": access_modes.split(','),
                    "storageClass": storage_class or None,
                    "size": size
                }

    def ask_service_questions(self):
        service_choice = self.get_input("是否要添加 Service? (yes/no): ", validation_func=lambda x: x in ['yes', 'no'])
        if service_choice == "yes":
            port = self.get_input("請輸入 Service 的 port (預設值: 80): ", allow_empty=True) or "80"
            target_port = self.get_input("請輸入 Service 的 targetPort (預設值: 8080): ", allow_empty=True) or "8080"
            self.service = {
                "port": port,
                "targetPort": target_port
            }


    def gather_input(self):
        '''
        基本問題：首先詢問最基本的問題，例如部署的名稱、映像檔名稱等。
        環境選擇：接著問用戶想為哪些環境生成配置。因為後面的設定可能會因環境而異。
        環境參數：為每個選定的環境詢問環境參數。
        HPA 和 VPA 問題：這些與擴展性相關的設定應在其他細節之前設定。
        ConfigMap 和 Secret：這些是更具體的部署設定，所以可以在最後詢問。
        '''
        self.ask_basic_questions()
        self.ask_service_questions()
        self.ask_environments_to_deploy()
        self.ask_environment_questions()
        self.ask_hpa_questions()
        self.ask_vpa_questions()
        self.ask_configmap_questions()
        self.ask_secret_questions()
        self.ask_storage_questions() 
        
