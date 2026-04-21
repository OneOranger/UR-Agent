from pathlib import Path
import yaml

from app.llm.prompt_registry import PromptRegistry


def load_yaml(path: str) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_registry():
    registry = PromptRegistry()

    assets = registry.get_assets()
    runtime = registry.get_runtime()
    versions = registry.get_versions()

    print("=== 校验开始 ===")

    # 1. 校验 runtime 和 versions 中的 task 是否都存在于 assets.task_prompts
    task_prompt_names = set(assets["task_prompts"].keys())
    runtime_task_names = set(runtime["runtime"].keys())
    version_task_names = set(versions["versions"].keys())
    mapping_task_names = set(assets["mappings"].keys())

    print("\n[1] 校验 task 名称一致性")
    print("task_prompts =", task_prompt_names)
    print("runtime =", runtime_task_names)
    print("versions =", version_task_names)
    print("mappings =", mapping_task_names)

    missing_in_assets = runtime_task_names - task_prompt_names
    missing_in_runtime = task_prompt_names - runtime_task_names
    missing_in_versions = task_prompt_names - version_task_names
    missing_in_mappings = task_prompt_names - mapping_task_names

    print("missing_in_assets =", missing_in_assets)
    print("missing_in_runtime =", missing_in_runtime)
    print("missing_in_versions =", missing_in_versions)
    print("missing_in_mappings =", missing_in_mappings)

    # 2. 校验 assets registry 中的路径文件是否存在
    print("\n[2] 校验 prompt 文件路径是否存在")
    all_paths = []
    all_paths.extend(assets["system_prompts"].values())
    all_paths.extend(assets["task_prompts"].values())
    all_paths.extend(assets["blocks"].values())

    for path in all_paths:
        exists = Path(path).exists()
        print(path, "exists =", exists)

    # 3. 校验 yaml metadata 是否完整
    print("\n[3] 校验 metadata 字段")
    required_fields = ["id", "name", "version", "owner", "description", "tags", "output_schema", "template"]

    for path in all_paths:
        data = load_yaml(path)

        # blocks 和 system 也允许 output_schema=none
        for field in required_fields:
            if field not in data:
                print(f"[MISSING FIELD] {path} -> {field}")

    # 4. 校验 versions.yaml 中 current 是否在 available 里
    print("\n[4] 校验 version 一致性")
    for task_name, config in versions["versions"].items():
        current = config["current"]
        available = config["available"]
        ok = current in available
        print(task_name, "current =", current, "available =", available, "ok =", ok)

    print("\n=== 校验结束 ===")


if __name__ == "__main__":
    validate_registry()