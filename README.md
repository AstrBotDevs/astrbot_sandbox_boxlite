# astrbot_sandbox_boxlite

Chinese version: [`README_cn.md`](./README_cn.md)

`astrbot_sandbox_boxlite` is an AstrBot sandbox runtime plugin that adds the `boxlite` provider.

It is intended for lightweight sandbox scenarios that do not need browser or GUI-specific tooling.

## Features

- Provides the `boxlite` sandbox runtime for AstrBot.
- Supports shell, Python, and filesystem operations.
- Syncs local AstrBot skills into the sandbox when the sandbox boots.
- Uses a lightweight runtime shape compared with more feature-rich remote providers.

## Requirements

- An AstrBot build that supports external sandbox provider plugins.
- The Python dependency from `requirements.txt`: `boxlite`.
- The Python `shipyard` package, because the Boxlite implementation reuses Shipyard-compatible filesystem wrappers.
- The local plugin source `data/plugins/astrbot_sandbox_shipyard`, because the current implementation imports a helper from that plugin.

## Installation

Clone the plugin into AstrBot's plugin directory:

```bash
git clone https://github.com/zouyonghe/astrbot_sandbox_boxlite.git data/plugins/astrbot_sandbox_boxlite
```

At the moment you should also keep the Shipyard plugin available locally:

```bash
git clone https://github.com/zouyonghe/astrbot_sandbox_shipyard.git data/plugins/astrbot_sandbox_shipyard
```

Then restart AstrBot or reload plugins.

## Configuration

Enable sandbox runtime in AstrBot and select this provider:

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

This plugin does not currently expose provider-specific configuration fields.

## Usage Notes

- Use this plugin when you want a lighter sandbox runtime and only need shell, Python, and filesystem behavior.
- It does not register browser tools.
- It does not register GUI tools such as screenshot, mouse, or keyboard tools.

## Limitations

- The current implementation reuses code from the Shipyard plugin, so `astrbot_sandbox_shipyard` should remain present in the same `data/plugins` tree.
- Browser automation is not included.
- GUI-specific tools are not included.

## Repository

- GitHub: https://github.com/zouyonghe/astrbot_sandbox_boxlite
