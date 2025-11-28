import os
import json
import logging
import subprocess

from infra_terraform import config

class Main:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def get_terraform_version(self):
        try:
            terraform_version = subprocess.check_output(['terraform', '-v']).decode('utf-8').strip()
            self.logger.info(f'Terraform version: {terraform_version}')
            return terraform_version
        except Exception as e:
            self.logger.error(f'Failed to get Terraform version: {e}')
            return None

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config_data = json.load(f)
                self.logger.info(f'Loaded config: {config_data}')
                return config_data
        except Exception as e:
            self.logger.error(f'Failed to load config: {e}')
            return None

    def main(self):
        terraform_version = self.get_terraform_version()
        if terraform_version is None:
            return

        config_data = self.load_config()
        if config_data is None:
            return

        os.mkdir('terraform')
        with open(os.path.join('terraform', 'config.json'), 'w') as f:
            json.dump(config_data, f, indent=4)

        try:
            subprocess.run(['terraform', 'init'], cwd='terraform')
            self.logger.info('Terraform initialized')
        except Exception as e:
            self.logger.error(f'Failed to initialize Terraform: {e}')

        try:
            subprocess.run(['terraform', 'apply', '-auto-approve'], cwd='terraform')
            self.logger.info('Terraform applied')
        except Exception as e:
            self.logger.error(f'Failed to apply Terraform: {e}')

if __name__ == "__main__":
    main = Main()
    main.main()