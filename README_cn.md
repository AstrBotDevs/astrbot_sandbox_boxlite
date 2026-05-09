# astrbot_sandbox_boxlite

英文版说明：[`README.md`](./README.md)

`astrbot_sandbox_boxlite` 是一个为 AstrBot 提供 `boxlite` 运行时的插件。

它适合不需要浏览器或 GUI 工具、只希望使用轻量沙箱能力的场景。

## 功能特性

- 为 AstrBot 提供 `boxlite` 沙箱运行时。
- 支持 shell、Python、文件系统操作。
- 沙箱启动时会同步本地 AstrBot skills。
- 相比功能更重的远程 provider，运行时形态更轻量。

## 依赖要求

- 需要使用已经支持外部 sandbox provider 插件的 AstrBot 版本。
- 依赖 `requirements.txt` 中的 `boxlite`。
- 需要 Python `shipyard` 包，因为当前 Boxlite 实现复用了兼容 Shipyard 的文件系统包装逻辑。
- 需要本地同时存在 `data/plugins/astrbot_sandbox_shipyard`，因为当前实现会直接导入其中的 helper。

## 安装方式

把插件克隆到 AstrBot 的插件目录：

```bash
git clone https://github.com/zouyonghe/astrbot_sandbox_boxlite.git data/plugins/astrbot_sandbox_boxlite
```

当前实现下，建议同时保留 Shipyard 插件源码：

```bash
git clone https://github.com/zouyonghe/astrbot_sandbox_shipyard.git data/plugins/astrbot_sandbox_shipyard
```

然后重启 AstrBot，或重新加载插件。

## 配置方法

先在 AstrBot 核心配置中启用 sandbox，并把运行时设置为 `boxlite`：

```json
{
  "provider_settings": {
    "computer_use_runtime": "sandbox",
    "sandbox": {
      "booter": "boxlite"
    }
  }
}
```

这个插件当前没有额外的 provider 专属配置项。

## 使用说明

- 当你只需要 shell、Python、文件系统能力，并希望运行时更轻量时，可以优先使用这个插件。
- 它不会注册浏览器工具。
- 它不会注册截图、鼠标、键盘等 GUI 工具。

## 限制说明

- 当前实现会复用 Shipyard 插件中的代码，因此 `astrbot_sandbox_shipyard` 需要与它一起存在于同一个 `data/plugins` 目录树中。
- 不包含浏览器自动化能力。
- 不包含 GUI 工具能力。

## 仓库地址

- GitHub: https://github.com/zouyonghe/astrbot_sandbox_boxlite
