#!/usr/bin/env python3
"""
PlaysoutiOSSDK CI Script
- 扫描 Frameworks/*.xcframework
- 生成语义正确的 Package.swift
- 更新 README.md 中的 Embed 对照表
"""

import os
import glob
import subprocess
import pathlib

# ========== 基础配置 ==========
PACKAGE_NAME = "PlaysoutiOSSDK"
MIN_IOS_VERSION = "16"
README_PATH = pathlib.Path("README.md")

EMBED_TABLE_MARKER_START = "<!-- EMBED_TABLE_START -->"
EMBED_TABLE_MARKER_END = "<!-- EMBED_TABLE_END -->"

# ========== 工具函数 ==========
def framework_type(xcframework_path: str) -> str:
    """
    判断 xcframework 是 static 还是 dynamic
    """
    name = os.path.basename(xcframework_path).replace(".xcframework", "")

    # 常见二进制路径
    patterns = [
        f"{xcframework_path}/ios-arm64/{name}.framework/{name}",
        f"{xcframework_path}/ios-arm64/*.framework/{name}",
        f"{xcframework_path}/ios-arm64/**/{name}.a",
    ]

    binary_path = None
    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            binary_path = matches[0]
            break

    if not binary_path or not os.path.exists(binary_path):
        return "unknown"

    try:
        result = subprocess.run(
            ["file", binary_path],
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout

        if "current ar archive" in result or "ar archive" in result:
            return "static (Do Not Embed)"
        elif "dynamically linked" in result:
            return "dynamic (Embed & Sign)"
        else:
            return "unknown"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "unknown"


def collect_frameworks() -> list[str]:
    frameworks = sorted(glob.glob("Frameworks/*.xcframework"))
    if not frameworks:
        raise SystemExit("❌ Frameworks/ 目录下未找到任何 .xcframework")
    return frameworks


# ========== 主逻辑 ==========
def main():
    frameworks = collect_frameworks()

    # 所有 framework 名称
    all_framework_names: list[str] = []
    binary_target_blocks: list[str] = []

    for fw in frameworks:
        name = os.path.basename(fw).replace(".xcframework", "")
        all_framework_names.append(name)
        binary_target_blocks.append(
            f'        .binaryTarget(name: "{name}", path: "Frameworks/{name}.xcframework"),'
        )

    # ✅ App 依赖所有其他 framework
    app_dependencies = [
        f'                "{n}",' for n in all_framework_names if n != "App"
    ]

    # ========== 生成 Package.swift ==========
    package_swift = f'''// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "{PACKAGE_NAME}",
    platforms: [.iOS(.v{MIN_IOS_VERSION})],
    products: [
        .library(
            name: "{PACKAGE_NAME}",
            targets: ["App"]
        )
    ],
    targets: [
        // MARK: - Main SDK Target
        .binaryTarget(
            name: "App",
            path: "Frameworks/App.xcframework",
            dependencies: [
{chr(10).join(app_dependencies)}
            ]
        ),

        // MARK: - Dependencies
{chr(10).join(binary_target_blocks)}
    ]
)
'''

    pathlib.Path("Package.swift").write_text(package_swift)
    print("✅ Package.swift generated")

    # ========== 生成 Embed 对照表 ==========
    embed_lines = [
        "## XCFramework Embed 对照表",
        "",
        "| Framework | Type | Xcode Embed Setting |",
        "|---------|------|---------------------|",
    ]

    for fw in frameworks:
        name = os.path.basename(fw)
        ftype = framework_type(fw)
        embed = (
            "Do Not Embed"
            if "static" in ftype
            else "Embed & Sign"
        )
        embed_lines.append(f"| `{name}` | {ftype} | **{embed}** |")

    embed_table = "\n".join(embed_lines)

    # ========== 更新 README.md ==========
    readme_text = ""
    if README_PATH.exists():
        readme_text = README_PATH.read_text()

    if EMBED_TABLE_MARKER_START in readme_text and EMBED_TABLE_MARKER_END in readme_text:
        before, rest = readme_text.split(EMBED_TABLE_MARKER_START, 1)
        _, after = rest.split(EMBED_TABLE_MARKER_END, 1)
        new_readme = (
            before
            + EMBED_TABLE_MARKER_START
            + "\n"
            + embed_table
            + "\n"
            + EMBED_TABLE_MARKER_END
            + after
        )
    else:
        new_readme = (
            readme_text
            + "\n\n"
            + EMBED_TABLE_MARKER_START
            + "\n"
            + embed_table
            + "\n"
            + EMBED_TABLE_MARKER_END
        )

    README_PATH.write_text(new_readme)
    print("✅ README.md Embed 对照表已更新")
    print("\n🎉 CI 脚本执行完成")


if __name__ == "__main__":
    main()