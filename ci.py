#!/usr/bin/env python3
import os
import glob
import subprocess
import pathlib

# ========== 基础配置 ==========
PACKAGE_NAME = "PlaysoutSDK"
MIN_IOS_VERSION = "16.0"
README_PATH = pathlib.Path("README.md")
EMBED_TABLE_MARKER_START = "<!-- EMBED_TABLE_START -->"
EMBED_TABLE_MARKER_END = "<!-- EMBED_TABLE_END -->"

# ========== 工具函数 ==========
def framework_type(xcframework_path: str) -> str:
    """
    判断 xcframework 是 static 还是 dynamic
    """
    name = os.path.basename(xcframework_path).replace(".xcframework", "")
    bins = glob.glob(f"{xcframework_path}/ios-arm64/**/{name}", recursive=True)
    if not bins:
        return "unknown"

    result = subprocess.run(
        ["file", bins[0]],
        capture_output=True,
        text=True
    ).stdout

    if "current ar archive" in result:
        return "static (Do Not Embed)"
    elif "dynamically linked" in result:
        return "dynamic (Embed & Sign)"
    else:
        return "unknown"

# ========== 扫描 Frameworks ==========
frameworks = sorted(glob.glob("Frameworks/*.xcframework"))
if not frameworks:
    raise SystemExit("❌ Frameworks/ 目录下未找到任何 .xcframework")

targets = []
product_targets = []

for fw in frameworks:
    name = os.path.basename(fw).replace(".xcframework", "")
    targets.append(f'        .binaryTarget(name: "{name}", path: "{fw}")')
    product_targets.append(f'                "{name}"')

# ========== 生成 Package.swift ==========
package_swift = f"""// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "{PACKAGE_NAME}",
    platforms: [.iOS(.v{MIN_IOS_VERSION})],
    products: [
        .library(
            name: "{PACKAGE_NAME}",
            targets: [
{chr(10).join(product_targets)}
            ]
        )
    ],
    targets: [
{chr(10).join(targets)}
    ]
)
"""

pathlib.Path("Package.swift").write_text(package_swift)
print("✅ Package.swift regenerated")

# ========== 生成 Embed 对照表 ==========
embed_table_lines = [
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
    embed_table_lines.append(f"| `{name}` | {ftype} | **{embed}** |")

embed_table = "\n".join(embed_table_lines)

# ========== 更新 README.md ==========
readme_text = ""
if README_PATH.exists():
    readme_text = README_PATH.read_text()

new_readme = ""

if EMBED_TABLE_MARKER_START in readme_text and EMBED_TABLE_MARKER_END in readme_text:
    # 替换已有表格
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
    # README 不存在或无标记，追加
    new_readme = readme_text + "\n\n" + EMBED_TABLE_MARKER_START + "\n" + embed_table + "\n" + EMBED_TABLE_MARKER_END

README_PATH.write_text(new_readme)
print("✅ README.md Embed 对照表已更新")

print("\n🎉 CI 脚本执行完成")