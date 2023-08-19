import os
import shutil

from config.deployment_config import DeploymentConfig
from generator.yaml_generator import DeploymentYAMLGenerator
from generator.kustomization_generator import KustomizationGenerator

def main(output_path="."):
    config = DeploymentConfig()
    config.gather_input()
    
    # Create directories according to kustomize structure
    base_dir = os.path.join(output_path, "base")
    overlays_dir = os.path.join(output_path, "overlays")
    
    # Create base and overlays directories
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(overlays_dir, exist_ok=True)

    # Generate and save base yaml files
    base_yaml_files = DeploymentYAMLGenerator.generate_base_yaml_files(config)
    for filename, content in base_yaml_files.items():
        with open(os.path.join(base_dir, filename), "w") as file:
            file.write(content)

    # For each environment, create directories and save yamls
    for env in config.deploy_environments:
        env_dir = os.path.join(overlays_dir, env)
        os.makedirs(env_dir, exist_ok=True)
        env_yaml_files = DeploymentYAMLGenerator.generate_overlay_yaml_files(config, env)
        for filename, content in env_yaml_files.items():
            with open(os.path.join(env_dir, filename), "w") as file:
                file.write(content)

    # Generate and save base kustomization file
    base_kustomization_content = KustomizationGenerator.generate_base_kustomization(config)
    with open(os.path.join(base_dir, "kustomization.yaml"), "w") as file:
        file.write(base_kustomization_content)

    # For each environment, create directories and save kustomization file
    for env in config.deploy_environments:
        env_dir = os.path.join(overlays_dir, env)
        overlay_kustomization_content = KustomizationGenerator.generate_overlay_kustomization(config, env)
        with open(os.path.join(env_dir, "kustomization.yaml"), "w") as file:
            file.write(overlay_kustomization_content)

    # Copy the deploy.sh script to the output directory
    script_src_path = os.path.join(os.path.dirname(__file__), 'deploy.sh')
    script_dst_path = os.path.join(output_path, 'deploy.sh')
    shutil.copy2(script_src_path, script_dst_path)

    print(f"Configuration for {config.name} has been generated under {output_path}")
    print("\n---------------------")
    print("注意：這只是一個範本。請根據您的具體需求進行調整和驗證，並在部署到集群之前手動檢查生成的 YAML 文件。")
    print("---------------------")

# If the script is the main entry point, parse the arguments and call the main function
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Kubernetes YAML configurations.")
    parser.add_argument("-o", "--output", type=str, default=".", help="Output directory for generated YAML files.")
    args = parser.parse_args()
    main(args.output)
