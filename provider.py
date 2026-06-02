from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from astrbot.core.computer.booters.base import ComputerBooter
from astrbot.core.star.context import Context

from .booters import boxlite as boxlite_booter
from .booters.boxlite import (
    DEFAULT_BOXLITE_NETWORK_MODE,
    BoxliteBooter,
    allocate_boxlite_host_port,
    normalize_boxlite_network_allow,
)

BootHook = Callable[[Context, str, str, dict], Awaitable[ComputerBooter]]


class BoxliteSandboxProvider:
    provider_id = "boxlite"
    capabilities = {"shell", "python", "filesystem"}
    supports_persistent_reconnect = True
    auto_sync_skills = False
    tool_names: set[str] = set()

    def __init__(
        self,
        boot_hook: BootHook | None = None,
        *,
        plugin_config: Mapping[str, Any] | None = None,
    ) -> None:
        self.plugin_config: dict[str, Any] = (
            dict(plugin_config) if plugin_config is not None else {}
        )
        self._boot_hook = boot_hook

    @staticmethod
    def _persistent_name(config: dict, fallback: str) -> str:
        return str(config.get("persistent_name") or fallback).strip()

    def build_create_config(self, context: Context, session_id: str) -> dict:
        network_mode = self._network_mode()
        network_allow = self._network_allow()
        return {
            "host_port": allocate_boxlite_host_port(),
            "network_mode": network_mode,
            "network_allow": network_allow,
        }

    def build_connect_info(self, sandbox_name: str, config: dict) -> dict:
        network_mode = self._network_mode(config)
        network_allow = self._network_allow(config)
        return {
            "name": sandbox_name,
            "persistent_name": self._persistent_name(
                config,
                str(config.get("sandbox_id") or sandbox_name),
            ),
            "host_port": int(config.get("host_port") or allocate_boxlite_host_port()),
            "network_mode": network_mode,
            "network_allow": network_allow,
        }

    def update_connect_info(self, record: dict, *, sandbox_name: str) -> dict:
        connect_info = dict(record.get("connect_info") or {})
        connect_info["name"] = sandbox_name
        connect_info.setdefault(
            "persistent_name",
            str(record.get("sandbox_id") or sandbox_name).strip(),
        )
        config = record.get("config")
        connect_info.setdefault("network_mode", self._network_mode(config))
        connect_info.setdefault("network_allow", self._network_allow(config))
        return connect_info

    def _network_mode(self, config: Mapping[str, Any] | None = None) -> str:
        config = config or {}
        mode = config.get("network_mode", self.plugin_config.get("network_mode"))
        mode = str(mode or "").strip()
        return mode or DEFAULT_BOXLITE_NETWORK_MODE

    def _network_allow(self, config: Mapping[str, Any] | None = None) -> list[str]:
        config = config or {}
        value = config.get("network_allow", self.plugin_config.get("network_allow"))
        if isinstance(value, str):
            value = value.split(",")
        return normalize_boxlite_network_allow(value)

    def update_connect_info_after_boot(
        self, record: dict, booter: ComputerBooter
    ) -> dict | None:
        host_port = getattr(booter, "host_port", None)
        if not host_port:
            return None
        connect_info = dict(record.get("connect_info") or {})
        connect_info["host_port"] = int(host_port)
        return connect_info

    def get_idle_timeout(self, context: Context, session_id: str) -> float:
        return 0.0

    async def check_persistent_sandbox_exists(self, record: dict) -> bool:
        connect_info = dict(record.get("connect_info") or {})
        box_name = str(
            connect_info.get("persistent_name")
            or connect_info.get("name")
            or record.get("sandbox_id")
            or ""
        ).strip()
        if not box_name:
            return False
        runtime = boxlite_booter.boxlite.Boxlite.default()
        return runtime.get_info(box_name) is not None

    async def create_booter(
        self, context: Context, session_id: str, sandbox_id: str, config: dict
    ) -> ComputerBooter:
        if self._boot_hook is not None:
            return await self._boot_hook(context, session_id, sandbox_id, config)
        host_port = config.get("host_port")
        if bool(config.get("resume", False)) and not host_port:
            raise RuntimeError(
                "Boxlite persistent sandbox cannot be resumed without a stored host_port"
            )
        network_mode = self._network_mode(config)
        network_allow = self._network_allow(config)
        client = BoxliteBooter(
            persistent=True,
            persistent_name=self._persistent_name(config, sandbox_id),
            resume=bool(config.get("resume", False)),
            sandbox_id=sandbox_id,
            host_port=int(host_port) if host_port else None,
            network_mode=network_mode,
            network_allow=network_allow,
        )
        await client.boot(uuid.uuid5(uuid.NAMESPACE_DNS, session_id).hex)
        return client

    async def destroy_booter(self, booter: ComputerBooter, record: dict) -> None:
        destroy = getattr(booter, "destroy", None)
        if callable(destroy):
            await destroy()
            return
        await booter.shutdown()
