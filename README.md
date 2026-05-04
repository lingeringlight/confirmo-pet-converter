# Confirmo Pet Converter.skill

[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111111?style=flat-square)](https://github.com/openai/codex)
[![Source](https://img.shields.io/badge/source-sprites.confirmo.love-18a058?style=flat-square)](https://sprites.confirmo.love/sprite)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

**Language / 语言**: [中文](#中文说明) · [English](#english-version)

## 中文说明

`confirmo-pet-converter` 是一个 Codex skill，用来把从 [sprites.confirmo.love/sprite](https://sprites.confirmo.love/sprite) 下载的桌宠形象包转换成 Codex App 可以识别的本地桌宠。

常见下载包结构是：

```text
manifest.json
sprite.png
```

转换后会生成：

```text
pet.json
spritesheet.webp
```

最终图集规格为 `1536x1872`，包含 `8x9` 个格子，每格 `192x208`。脚本会自动去掉常见的粉色/洋红色背景，并把结果写入 Codex 桌宠目录。

## 适合谁用

如果你已经从 Confirmo sprite 站点下载了角色包，但把文件夹放进 `~/.codex/pets` 后 Codex 没有显示它，这个 skill 就是为这个场景准备的。

它适合：

- 把 Confirmo 角色包导入 Codex 桌宠选择器
- 去掉 sprite 图的纯色背景
- 批量转换 `~/.codex/pets` 下多个下载包
- 给每个角色补齐 Codex 需要的 `pet.json`

## 安装

把这个仓库安装到 Codex skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R confirmo-pet-converter "${CODEX_HOME:-$HOME/.codex}/skills/"
```

如果 skill 列表没有立刻刷新，重启 Codex App。

你也可以让 Codex 从 GitHub 仓库安装：

```text
使用 $skill-installer，从 https://github.com/lingeringlight/confirmo-pet-converter 安装 skill。
```

## 使用方法

转换单个已下载角色包：

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/confirmo-pet-converter/scripts/convert_confirmo_pet.py" \
  --pet-dir "${CODEX_HOME:-$HOME/.codex}/pets/ikun"
```

批量转换 Codex pets 目录下所有 Confirmo 风格包：

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/confirmo-pet-converter/scripts/convert_confirmo_pet.py" \
  --all "${CODEX_HOME:-$HOME/.codex}/pets"
```

也可以直接在 Codex 里说：

```text
使用 $confirmo-pet-converter，把 ~/.codex/pets 下面从 https://sprites.confirmo.love/sprite 下载的桌宠包全部转换成 Codex 可识别格式。
```

## 输入要求

单个角色文件夹里至少需要有：

```text
manifest.json
sprite.png
```

推荐放在：

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/
```

例如：

```text
~/.codex/pets/ikun/
  manifest.json
  sprite.png
```

## 输出结果

转换成功后同一个文件夹会包含：

```text
~/.codex/pets/ikun/
  manifest.json
  sprite.png
  pet.json
  spritesheet.webp
  _conversion_qa/
```

其中：

- `pet.json` 是 Codex 桌宠配置
- `spritesheet.webp` 是 Codex 使用的透明背景动画图集
- `_conversion_qa/` 保存转换检查文件和预览

完成后如果宠物没有立刻出现，重启 Codex App 或重新打开桌宠选择器。

## 常见问题

**为什么我把下载的文件夹放进 `~/.codex/pets` 之后没有显示？**

Codex 需要 `pet.json` 和符合固定规格的 `spritesheet.webp`。Confirmo 下载包通常只有 `manifest.json` 和 `sprite.png`，所以需要先转换。

**为什么要去背景？**

桌宠在桌面上需要透明背景。如果原始 sprite 使用粉色/洋红色背景，不去掉的话会显示成一块色块。

**可以批量处理吗？**

可以，用 `--all` 指向 pets 根目录即可。

## 许可证

MIT。请同时遵守你下载的角色素材本身的来源和授权要求。

---

## English Version

`confirmo-pet-converter` is a Codex skill for converting desktop pet sprite packages downloaded from [sprites.confirmo.love/sprite](https://sprites.confirmo.love/sprite) into local pet packages recognized by the Codex App.

A typical downloaded package contains:

```text
manifest.json
sprite.png
```

This skill converts it into:

```text
pet.json
spritesheet.webp
```

The generated atlas is `1536x1872`, with an `8x9` grid of `192x208` cells. The converter removes the common pink/magenta chroma-key background and writes the files Codex expects.

## Who Is This For

Use this skill when you downloaded a character package from the Confirmo sprite site, placed it under `~/.codex/pets`, and Codex did not show it in the desktop pet picker.

It helps you:

- import Confirmo character packages into the Codex desktop pet picker
- remove the solid sprite background
- batch-convert multiple downloaded packages
- create the required `pet.json` configuration

## Installation

Copy this repository into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R confirmo-pet-converter "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex App if the skill list does not refresh immediately.

You can also ask Codex to install it from GitHub:

```text
Use $skill-installer to install the skill from https://github.com/lingeringlight/confirmo-pet-converter.
```

## Usage

Convert one downloaded pet package:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/confirmo-pet-converter/scripts/convert_confirmo_pet.py" \
  --pet-dir "${CODEX_HOME:-$HOME/.codex}/pets/ikun"
```

Convert every Confirmo-style package under your Codex pets folder:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/confirmo-pet-converter/scripts/convert_confirmo_pet.py" \
  --all "${CODEX_HOME:-$HOME/.codex}/pets"
```

Or ask Codex directly:

```text
Use $confirmo-pet-converter to convert all desktop pet packages downloaded from https://sprites.confirmo.love/sprite under ~/.codex/pets into Codex-compatible pets.
```

## Input Requirements

Each source pet folder must contain at least:

```text
manifest.json
sprite.png
```

Recommended location:

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/
```

Example:

```text
~/.codex/pets/ikun/
  manifest.json
  sprite.png
```

## Output

After conversion, the same folder will contain:

```text
~/.codex/pets/ikun/
  manifest.json
  sprite.png
  pet.json
  spritesheet.webp
  _conversion_qa/
```

The important files are:

- `pet.json`: Codex desktop pet metadata
- `spritesheet.webp`: transparent animated atlas used by Codex
- `_conversion_qa/`: validation and preview artifacts

If the pet does not appear immediately, restart Codex App or reopen the desktop pet picker.

## FAQ

**Why does nothing show up after I copy the downloaded folder into `~/.codex/pets`?**

Codex expects `pet.json` plus a fixed-size `spritesheet.webp`. Confirmo downloads usually contain only `manifest.json` and `sprite.png`, so they need conversion first.

**Why remove the background?**

Desktop pets need transparent backgrounds. If the original sprite uses a pink or magenta chroma-key background, leaving it in place will show a colored block around the pet.

**Can I convert multiple packages at once?**

Yes. Use `--all` with your pets root directory.

## License

MIT. Please also respect the source and license terms of the character assets you download.
