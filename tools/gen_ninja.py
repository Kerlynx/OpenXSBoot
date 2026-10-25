#!/usr/bin/env python3
"""OpenXSBoot 独立构建：生成只产出引导 out/BOOTX64.efi 的 build.ninja。"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find(base, suffixes):
    root = ROOT / base
    if not root.exists():
        return []
    return sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in suffixes)


def esc(p):
    return str(p).replace("$", "$$").replace(":", "$:").replace(" ", "$ ")


def main():
    cc = os.environ.get("BOOT_CC", "x86_64-w64-mingw32-gcc")
    color = os.environ.get("DIAGNOSTICS_COLOR", "-fdiagnostics-color=always")
    boot_flags = (f"{color} -g -I ./boot/include -Wextra -e efi_main -nostdinc -nostdlib "
                  "-fno-builtin -Wl,--subsystem,10 -fshort-wchar")

    headers = [p.relative_to(ROOT) for p in find("boot/include", (".h", ".hpp"))]
    hstr = " ".join(esc(h) for h in headers)

    L = ["# OpenXSBoot 专用：只构建 UEFI 引导", "ninja_required_version = 1.10",
         f"cc = {cc}", f"boot_c_flags = {boot_flags}", "",
         "rule boot",
         "  command = mkdir -p $$(dirname $out) && $cc $boot_c_flags -o $out $in", ""]

    edge = "build out/BOOTX64.efi: boot boot/bootx64.c boot/bootlib.c"
    if hstr:
        edge += f" | {hstr}"
    L += [edge, ""]

    # ---- xbps 打包（pack）----
    pkg = {"name": "OpenXSBoot", "ver": "2.1_1", "arch": "x86_64",
           "desc": "Leopard UEFI bootloader", "install": "EFI/BOOT/BOOTX64.EFI"}
    pkg_args = f"-A {pkg['arch']} -n {pkg['name']}-{pkg['ver']} -s '{pkg['desc']}'"
    xbps_out = f"out/{pkg['name']}-{pkg['ver']}.{pkg['arch']}.xbps"
    L += [
        "rule package",
        f"  command = rm -rf .pkg && mkdir -p .pkg/$$(dirname {pkg['install']}) && "
        f"cp out/BOOTX64.efi .pkg/{pkg['install']} && cd out && xbps-create --compression gzip {pkg_args} ../.pkg",
        "",
        f"build {xbps_out}: package out/BOOTX64.efi",
        "build build: phony out/BOOTX64.efi",
        f"build pack: phony {xbps_out}",
        "default build", "",
        "rule clean", "  command = rm -rf out .pkg", "build clean: clean",
    ]

    (ROOT / "build.ninja").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("已生成 build.ninja（仅引导）。构建：ninja")


if __name__ == "__main__":
    main()

