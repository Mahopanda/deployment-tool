import os

from config.deployment_config import DeploymentConfig
from generator.yaml_generator import DeploymentYAMLGenerator

class KustomizationGenerator:

    @staticmethod
    def generate_base_kustomization(data: DeploymentConfig, output_path="."):
        resources = []

        resource_types = ['deployment', 'hpa', 'vpa', 'service', 'pv', 'pvc', 'configMap', 'secret']
        for resource_type in resource_types:
            resource_content = DeploymentYAMLGenerator.generate_base_yaml_files(data).get(f'{resource_type}.yaml')
            if resource_content:
                resources.append(f"{resource_type}.yaml")

        base_kustomization_content = """
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
        """
        for resource in resources:
            base_kustomization_content += f"- {resource}\n"

        return base_kustomization_content


    @staticmethod
    def generate_overlay_kustomization(data: DeploymentConfig, env):
        resources = ["../../base"]  # Default base resource
        patches = []

        # Check for environment-specific changes in various resources
        resource_types = ['deployment', 'hpa', 'vpa', 'service', 'pv', 'pvc', 'configMap', 'secret']
        for resource_type in resource_types:
            overlay_content = DeploymentYAMLGenerator.generate_overlay_yaml_files(data, env).get(f'{resource_type}.yaml')
            if overlay_content:
                patches.append(f"{resource_type}.yaml")

        # Construct the overlay kustomization content
        overlay_kustomization_content = f"""
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

bases:
        """
        for resource in resources:
            overlay_kustomization_content += f"- {resource}\n"

        if patches:
            overlay_kustomization_content += "\npatchesStrategicMerge:\n"
            for patch in patches:
                overlay_kustomization_content += f"- {patch}\n"

        overlay_kustomization_content += f"\nnameSuffix: -{env}\n"

        return overlay_kustomization_content


    @staticmethod
    def generate_all(environments=["dev", "stage", "prod"], output_path="."):
        KustomizationGenerator.generate_base_kustomization(output_path)
        for env in environments:
            KustomizationGenerator.generate_overlay_kustomization(env, output_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate kustomization.yaml files for Kubernetes deployments.")
    parser.add_argument("-o", "--output", type=str, default=".", help="Output directory for generated files.")
    parser.add_argument("-e", "--environments", nargs='+', default=["dev", "stage", "prod"], help="List of environments to generate overlays for.")
    args = parser.parse_args()
    KustomizationGenerator.generate_all(args.environments, args.output)
