from pathlib import Path
import yaml


class PromptRegistry:
    """
    Prompt 注册表管理器

    作用：
    1. 读取 assets registry
    2. 读取 runtime registry
    3. 查询某个 task 当前是否启用
    4. 查询某个 task 当前用哪个版本
    """

    def __init__(
        self,
        assets_path: str = "app/prompts/registry.assets.yaml",
        runtime_path: str = "app/prompts/registry.runtime.yaml",
        versions_path: str = "app/prompts/versions.yaml",
    ):
        self.assets_path = Path(assets_path)
        self.runtime_path = Path(runtime_path)
        self.versions_path = Path(versions_path)

        self.assets = self._load_yaml(self.assets_path)
        self.runtime = self._load_yaml(self.runtime_path)
        self.versions = self._load_yaml(self.versions_path)

    def _load_yaml(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def is_enabled(self, task_name: str) -> bool:
        """
        查询某个 task 当前是否启用
        """
        return self.runtime["runtime"][task_name]["enabled"]

    def get_runtime_version(self, task_name: str) -> str:
        """
        查询 runtime 当前配置版本
        """
        return self.runtime["runtime"][task_name]["version"]

    def get_current_version(self, task_name: str) -> str:
        """
        查询 versions.yaml 中声明的当前版本
        """
        return self.versions["versions"][task_name]["current"]

    def get_assets(self) -> dict:
        return self.assets

    def get_runtime(self) -> dict:
        return self.runtime

    def get_versions(self) -> dict:
        return self.versions