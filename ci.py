#!/usr/bin/env python3
"""
PlaysoutiOSSDK CI 构建脚本
- 自动扫描 Frameworks/*.xcframework
- 生成符合 SPM 规范的 Package.swift（采用 target 包装层承载依赖，解决 binaryTarget 无法声明依赖的问题）
- 自动更新 README 中的 XCFramework 嵌入对照表
"""

import os
import glob
import subprocess
import pathlib

# ========== 基础配置（和提供的 Package.swift 完全对齐） ==========
PACKAGE_NAME = "PlaysoutiOSSDK"
WRAPPER_TARGET_NAME = "PlaysoutiOSSDKFramework"  # 对外暴露的中间 target
MIN_IOS_VERSION = "16"
README_PATH = pathlib.Path("README.md")

EMBED_TABLE_MARKER_START = "<!-- EMBED_TABLE_START -->"
EMBED_TABLE_MARKER_END = "<!-- EMBED_TABLE_END -->"

# ========== 工具函数 ==========
def detect_framework_type(xcframework_path: str) -> str:
    """检测 xcframework 是静态库还是动态库"""
    framework_name = os.path.basename(xcframework_path).replace(".xcframework", "")

    # 优先查找常见的二进制路径
    search_patterns = [
        f"{xcframework_path}/ios-arm64/{framework_name}.framework/{framework_name}",
        f"{xcframework_path}/ios-arm64/*.framework/{framework_name}",
        f"{xcframework_path}/ios-arm64/**/{framework_name}.a",
    ]

    binary_path = None
    for pattern in search_patterns:
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


def collect_all_frameworks() -> list[str]:
    """扫描所有 xcframework，返回排序后的框架名称列表"""
    xcframeworks = sorted(glob.glob("Frameworks/*.xcframework"))
    if not xcframeworks:
        raise SystemExit("❌ Frameworks/ 目录下未找到任何 .xcframework")

    framework_names = []
    for xcframework in xcframeworks:
        name = os.path.basename(xcframework).replace(".xcframework", "")
        framework_names.append(name)
    return framework_names


# ========== 主逻辑 ==========
def main():
    # 1. 扫描所有框架
    all_framework_names = collect_all_frameworks()
    print(f"✅ 扫描到 {len(all_framework_names)} 个 XCFramework")

    # 2. 生成 wrapper target 的依赖列表（所有 binaryTarget 都需要作为它的依赖）
    wrapper_dependencies = [
        f'                "{name}",' for name in all_framework_names
    ]

    # 3. 生成所有 binaryTarget 的定义
    binary_target_blocks = [
        f'        .binaryTarget(name: "{name}", path: "Frameworks/{name}.xcframework"),'
        for name in all_framework_names
    ]

    # ========== 生成 Package.swift（和你提供的结构 100% 对齐） ==========
    package_swift_content = f'''// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "{PACKAGE_NAME}",
    platforms: [.iOS(.v{MIN_IOS_VERSION})],
    products: [
        .library(
            name: "{PACKAGE_NAME}",
            targets: ["{WRAPPER_TARGET_NAME}"]
        )
    ],
    targets: [
        // MARK: - 对外暴露的中间 Target（承载所有依赖，无实际源码）
        .target(
            name: "{WRAPPER_TARGET_NAME}",
            dependencies: [
{chr(10).join(wrapper_dependencies)}
            ]
        ),

        // MARK: - 所有预编译依赖
{chr(10).join(binary_target_blocks)}
    ]
)
'''
    pathlib.Path("Package.swift").write_text(package_swift_content)
    print("✅ Package.swift 生成成功")

    # ========== 生成 XCFramework 嵌入对照表 ==========
    embed_table_lines = [
        "## XCFramework Embed 对照表",
        "",
        "| Framework | 类型 | Xcode 嵌入设置 |",
        "|---------|------|----------------|",
    ]

    for framework_name in all_framework_names:
        xcframework_path = f"Frameworks/{framework_name}.xcframework"
        framework_type = detect_framework_type(xcframework_path)
        embed_setting = (
            "Do Not Embed"
            if "static" in framework_type
            else "Embed & Sign"
        )
        embed_table_lines.append(
            f"| `{framework_name}.xcframework` | {framework_type} | **{embed_setting}** |"
        )

    embed_table = "\n".join(embed_table_lines)

    # ========== 更新 README.md ==========
    readme_content = ""
    if README_PATH.exists():
        readme_content = README_PATH.read_text()

    if EMBED_TABLE_MARKER_START in readme_content and EMBED_TABLE_MARKER_END in readme_content:
        # 替换已有表格
        before, rest = readme_content.split(EMBED_TABLE_MARKER_START, 1)
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
        # 首次添加表格
        new_readme = (
            readme_content
            + "\n\n"
            + EMBED_TABLE_MARKER_START
            + "\n"
            + embed_table
            + "\n"
            + EMBED_TABLE_MARKER_END
        )

    README_PATH.write_text(new_readme)
    print("✅ README.md 嵌入对照表更新成功")
    print("\n🎉 CI 脚本执行完成")


if __name__ == "__main__":
    main()