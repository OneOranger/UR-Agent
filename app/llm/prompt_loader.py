from pathlib import Path
import re
import yaml

from app.llm.prompt_registry import PromptRegistry


class PromptLoader:
    """
    Prompt 统一加载器

    功能：
    1. 读取 assets registry
    2. 读取 runtime / version registry
    3. 读取 system / task / blocks yaml
    4. 渲染变量
    5. 拼接成最终 prompt
    6. 支持读取 prompt metadata
    """

    def __init__(self, registry_path: str = "app/prompts/registry.assets.yaml"):
        self.registry = PromptRegistry(
            assets_path=registry_path,
            runtime_path="app/prompts/registry.runtime.yaml",
            versions_path="app/prompts/versions.yaml",
        )
        self.assets = self.registry.get_assets()

    def _load_yaml(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _render_template(self, template: str, variables: dict) -> str:
        rendered = template
        for key, value in variables.items():
            rendered = re.sub(r"{{\s*" + re.escape(key) + r"\s*}}", str(value), rendered)
        return rendered

    def _load_prompt_file(self, relative_path: str) -> dict:
        """
        读取完整 prompt 文件，返回完整 dict
        """
        path = Path(relative_path)
        return self._load_yaml(path)

    def get_prompt_metadata(self, task_name: str) -> dict:
        """
        获取某个 task 对应的 metadata
        """
        mapping = self.assets["mappings"][task_name]

        system_name = mapping["system"]
        block_names = mapping.get("blocks", [])

        system_path = self.assets["system_prompts"][system_name]
        task_path = self.assets["task_prompts"][task_name]

        system_file = self._load_prompt_file(system_path)
        task_file = self._load_prompt_file(task_path)

        block_files = []
        for block_name in block_names:
            block_path = self.assets["blocks"][block_name]
            block_files.append(self._load_prompt_file(block_path))

        return {
            "task": {
                "id": task_file.get("id"),
                "name": task_file.get("name"),
                "version": task_file.get("version"),
                "owner": task_file.get("owner"),
                "description": task_file.get("description"),
                "tags": task_file.get("tags", []),
                "output_schema": task_file.get("output_schema"),
            },
            "system": {
                "id": system_file.get("id"),
                "name": system_file.get("name"),
                "version": system_file.get("version"),
                "owner": system_file.get("owner"),
                "description": system_file.get("description"),
                "tags": system_file.get("tags", []),
            },
            "blocks": [
                {
                    "id": block_file.get("id"),
                    "name": block_file.get("name"),
                    "version": block_file.get("version"),
                    "owner": block_file.get("owner"),
                    "description": block_file.get("description"),
                    "tags": block_file.get("tags", []),
                }
                for block_file in block_files
            ],
        }

    def build_prompt(self, task_name: str, variables: dict) -> str:
        """
        根据 task_name 构建最终 prompt
        """
        if not self.registry.is_enabled(task_name):
            raise ValueError(f"Prompt task is disabled: {task_name}")

        mapping = self.assets["mappings"][task_name]

        system_name = mapping["system"]
        block_names = mapping.get("blocks", [])

        system_path = self.assets["system_prompts"][system_name]
        task_path = self.assets["task_prompts"][task_name]

        system_file = self._load_prompt_file(system_path)
        task_file = self._load_prompt_file(task_path)

        system_template = system_file["template"]
        task_template = task_file["template"]

        block_templates = []
        for block_name in block_names:
            block_path = self.assets["blocks"][block_name]
            block_file = self._load_prompt_file(block_path)
            block_templates.append(block_file["template"])

        rendered_task = self._render_template(task_template, variables)

        version = self.registry.get_current_version(task_name)

        parts = [
            f"[PromptTask={task_name}][Version={version}]",
            system_template,
        ]
        parts.extend(block_templates)
        parts.append(rendered_task)

        return "\n\n".join(parts)