#!/usr/bin/env python3
"""
修复 OpenRouter 模型页面中的 ~ 前缀问题
"""

import os
import re
import shutil
from pathlib import Path

# 正确的厂商映射（移除 ~ 前缀）
VENDOR_CLEANUP = {
    "~Openai": "OpenAI",
    "~Anthropic": "Anthropic",
    "~Google": "Google",
    "~Deepseek": "DeepSeek",
    "~Moonshotai": "月之暗面",
    "~X-Ai": "xAI",
    "~Z-Ai": "智谱 AI",
    "~MiniMax": "MiniMax",
    "~Mistral AI": "Mistral AI",
    "~Amazon": "Amazon",
    "~Cohere": "Cohere",
    "~OpenRouter": "OpenRouter",
    "~Inference": "Inference.net",
}

def fix_model_page(filepath):
    """修复单个模型页面中的 ~ 问题"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 修复 title 字段中的 ~
    old_content = content
    for old_vendor, new_vendor in VENDOR_CLEANUP.items():
        # 修复 vendor 字段
        content = content.replace(f'vendor: "{old_vendor}"', f'vendor: "{new_vendor}"')
        # 修复 title 字段
        content = content.replace(f'title: "{old_vendor}', f'title: "{new_vendor}')
        content = content.replace(f'title: "{old_vendor}', f'title: "{new_vendor}')

    # 清理 title 中的 ~ 前缀
    for old_name in VENDOR_CLEANUP.keys():
        new_name = VENDOR_CLEANUP[old_name]
        content = content.replace(f'title: "{old_name} ', f'title: "{new_name} ')

    # 如果有修改，写回文件
    if content != old_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        return True
    return False

def fix_file_paths():
    """修复文件路径中的 ~"""
    models_dir = Path("content/models/openrouter")

    for old_dir in models_dir.iterdir():
        if old_dir.is_dir() and old_dir.name.startswith('~'):
            new_name = old_dir.name[1:]  # 移除 ~ 前缀
            new_dir = models_dir / new_name

            # 如果新目录不存在，重命名
            if not new_dir.exists():
                try:
                    old_dir.rename(new_dir)
                    print(f"Renamed: {old_dir.name} -> {new_name}")

                    # 重命名文件
                    old_file = new_dir / "_index.md"
                    if old_file.exists():
                        fix_model_page(old_file)

                except Exception as e:
                    print(f"Error renaming {old_dir.name}: {e}")
            else:
                print(f"Skip: {new_name} already exists")

def main():
    print("开始修复 OpenRouter 模型页面中的 ~ 问题...")

    # 修复文件路径
    fix_file_paths()

    # 修复所有模型页面
    models_dir = Path("content/models/openrouter")
    fixed_count = 0

    for model_file in models_dir.rglob("_index.md"):
        if fix_model_page(model_file):
            fixed_count += 1

    print(f"\n完成！修复了 {fixed_count} 个模型页面。")

if __name__ == "__main__":
    main()