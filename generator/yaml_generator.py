from templates import base, hpa, vpa, configmap, secret, pv, pvc, service
from config.deployment_config import DeploymentConfig
import base64


class DeploymentYAMLGenerator:

    

    @staticmethod
    def generate_hpa_yaml(data: DeploymentConfig, env=None):
        if not data.hpa:
            return ""
        return hpa.hpa_yaml_template.format(
            name=data.name,
            namespace=data.namespace,
            min_pods=data.hpa.get("minPods", 1),
            max_pods=data.hpa.get("maxPods", 3),
            cpu_utilization=data.hpa.get("cpuUtilization", 80)
        )

    @staticmethod
    def generate_vpa_yaml(data: DeploymentConfig, env=None):
        if not data.vpa:
            return ""
        return vpa.vpa_yaml_template.format(name=data.name, namespace=data.namespace)

    @staticmethod
    def generate_pv_yaml(data: DeploymentConfig, env=None):
        if not data.pv:
            return ""
        return pv.pv_yaml_template.format(
            pv_name=f"{data.name}-pv",
            storage_class=data.pv["storageClass"],
            size=data.pv["size"],
            access_mode=data.pv.get("accessMode", "ReadWriteOnce")
        )

    @staticmethod
    def generate_pvc_yaml(data: DeploymentConfig, env=None):
        if not data.pvc:
            return ""
        return pvc.pvc_yaml_template.format(
            pvc_name=f"{data.name}-pvc",
            storage_class=data.pvc["storageClass"],
            size=data.pvc["size"],
            access_mode=data.pvc.get("accessMode", "ReadWriteOnce")
        )

    @staticmethod
    def generate_service_yaml(data: DeploymentConfig, env=None):
        # This is a basic example for a Service. You can expand on this based on your requirements.
        return service.service_yaml_template.format(
            name=data.name,
            namespace=data.namespace
        )

    @staticmethod
    def generate_configmap_yaml(data: DeploymentConfig, env=None):
        configmaps = ""
        for name, content in data.configmaps.items():
            formatted_data = "\n".join([f"  {k}: {v}" for k, v in content.items()])
            configmaps += configmap.configmap_template.format(name=name, namespace=data.namespace, data=formatted_data)
        return configmaps

    @staticmethod
    def generate_secret_yaml(data: DeploymentConfig, env=None):
        secrets = ""
        for name, content in data.secrets.items():
            # Now, we'll base64 encode these values.
            formatted_data = "\n".join([f"  {k}: {base64.b64encode(v.encode()).decode()}" for k, v in content.items()])
            secrets += secret.secret_template.format(name=name, namespace=data.namespace, data=formatted_data)
        return secrets

    @staticmethod
    def generate_base_yaml_files(data: DeploymentConfig, env=None):
        resource_methods = {
            'deployment.yaml': DeploymentYAMLGenerator.generate_base_yaml,
            'hpa.yaml': DeploymentYAMLGenerator.generate_hpa_yaml,
            'vpa.yaml': DeploymentYAMLGenerator.generate_vpa_yaml,
            'pv.yaml': DeploymentYAMLGenerator.generate_pv_yaml,
            'pvc.yaml': DeploymentYAMLGenerator.generate_pvc_yaml,
            'service.yaml': DeploymentYAMLGenerator.generate_service_yaml,
            'configMap.yaml': DeploymentYAMLGenerator.generate_configmap_yaml,
            'secret.yaml': DeploymentYAMLGenerator.generate_secret_yaml
        }

        # Filter out resources that are not applicable for the base (e.g., if no HPA is defined)
        resources_to_generate = [
            filename for filename, generator in resource_methods.items() if generator(data)
        ]

        generated_files = {}
        for filename in resources_to_generate:
            content = resource_methods[filename](data)
            if content:  # 只加入內容不為空的YAML文件
                generated_files[filename] = content

        return generated_files


    @staticmethod
    def generate_overlay_yaml_files(data: DeploymentConfig, env="dev"):
        resource_methods = {
            'deployment.yaml': DeploymentYAMLGenerator.generate_base_yaml,
            'hpa.yaml': DeploymentYAMLGenerator.generate_hpa_yaml,
            'vpa.yaml': DeploymentYAMLGenerator.generate_vpa_yaml,
            'pv.yaml': DeploymentYAMLGenerator.generate_pv_yaml,
            'pvc.yaml': DeploymentYAMLGenerator.generate_pvc_yaml,
            'service.yaml': DeploymentYAMLGenerator.generate_service_yaml,
            'configMap.yaml': DeploymentYAMLGenerator.generate_configmap_yaml,
            'secret.yaml': DeploymentYAMLGenerator.generate_secret_yaml
        }

        # Filter out resources that user has opted out of (for example, if they said 'no' to HPA)
        resources_to_generate = [
            filename for filename, generator in resource_methods.items() if generator(data, env)
        ]

        generated_files = {}
        for filename in resources_to_generate:
            content = resource_methods[filename](data, env)
            if content:  # 只加入內容不為空的YAML文件
                generated_files[filename] = content

        return generated_files


    @staticmethod
    def generate_overlay_patch(data: DeploymentConfig, env="dev"):
        """Generate environment-specific overlay patch."""
        return base.deployment_patch_yaml_template.format(
            name=data.name,
            cpu_request=data.environments[env]["cpuRequest"],
            memory_request=data.environments[env]["memoryRequest"],
            cpu_limit=data.environments[env]["cpuLimit"],
            memory_limit=data.environments[env]["memoryLimit"]
        )

    @staticmethod
    def generate_yaml_files(data: DeploymentConfig, env="dev"):
        resource_generators = {
            'deployment.yaml': DeploymentYAMLGenerator.generate_base_yaml,
            'hpa.yaml': DeploymentYAMLGenerator.generate_hpa_yaml,
            'vpa.yaml': DeploymentYAMLGenerator.generate_vpa_yaml,
            'pv.yaml': DeploymentYAMLGenerator.generate_pv_yaml,
            'pvc.yaml': DeploymentYAMLGenerator.generate_pvc_yaml,
            'service.yaml': DeploymentYAMLGenerator.generate_service_yaml,
            'configMap.yaml': DeploymentYAMLGenerator.generate_configmap_yaml,
            'secret.yaml': DeploymentYAMLGenerator.generate_secret_yaml
        }

        generated_files = {}
        for filename, generator in resource_generators.items():
            content = generator(data)
            if content:  # 只加入內容不為空的YAML文件
                generated_files[filename] = content

        return generated_files

    
    @staticmethod
    def generate_base_yaml(data: DeploymentConfig, env=None):
        return base.base_yaml_template.format(
            name=data.name,
            namespace=data.namespace,
            replicas=data.replicas,
            image=data.image,
            cpu_request=data.cpu_request,
            memory_request=data.memory_request,
            cpu_limit=data.cpu_limit,
            memory_limit=data.memory_limit,
        )

    @staticmethod
    def generate_patch_yaml(data: DeploymentConfig, env):
        return base.base_yaml_template.format(
            name=data.name,
            namespace=data.namespace,
            replicas=data.replicas,
            image=data.image,
            cpu_request=data.environments[env]["cpuRequest"],
            memory_request=data.environments[env]["memoryRequest"],
            cpu_limit=data.environments[env]["cpuLimit"],
            memory_limit=data.environments[env]["memoryLimit"]
        )
    
    @staticmethod
    def generate_base_resources(data: DeploymentConfig):
        return {
            'deployment.yaml': DeploymentYAMLGenerator.generate_base_yaml(data),
            'hpa.yaml': DeploymentYAMLGenerator.generate_hpa_yaml(data),
            'vpa.yaml': DeploymentYAMLGenerator.generate_vpa_yaml(data),
            'pv.yaml': DeploymentYAMLGenerator.generate_pv_yaml(data),
            'pvc.yaml': DeploymentYAMLGenerator.generate_pvc_yaml(data),
            'service.yaml': DeploymentYAMLGenerator.generate_service_yaml(data),
            'configMap.yaml': DeploymentYAMLGenerator.generate_configmap_yaml(data),
            'secret.yaml': DeploymentYAMLGenerator.generate_secret_yaml(data)
        }
    
    @staticmethod
    def generate_overlay_resources(data: DeploymentConfig, env):
        # For overlays, we only need the patch files. In this example, we're only generating a patch for the deployment.
        # But you can extend it to generate patches for other resources as needed.
        return {
            'deployment-patch.yaml': DeploymentYAMLGenerator.generate_patch_yaml(data, env)
        }