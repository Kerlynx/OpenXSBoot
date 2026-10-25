#pragma once
#define MAX_CPU_NUM 256

#define DEBUG_VERSION 0
#define RELEASE_VERSION 1
#if defined(CONFIG_BUILD_EDITION_RELEASE)
#define BUILD_EDITION RELEASE_VERSION
#else
#define BUILD_EDITION DEBUG_VERSION
#endif

/* 每 CPU 临时栈大小，必须与内核 build_settings.h 的 CONFIG_STACK_SIZE 保持一致 */
#define CONFIG_STACK_SIZE 262144
#define STACK_SIZE (CONFIG_STACK_SIZE * 1UL)

#ifndef _BOOT_H_
#define _BOOT_H_
#include <efi.h>
#include <memory.h>

#define MAX_CPU_NUM 256

#define BOOT_FLAG_SAFE_MODE        (1ULL << 0)
#define BOOT_FLAG_VERBOSE          (1ULL << 1)
#define BOOT_FLAG_DISABLE_KMOD     (1ULL << 2)
#define BOOT_FLAG_SAFE_STORAGE_IO  (1ULL << 3)
#define BOOT_FLAG_BASE_VIDEO       (1ULL << 4)
#define BOOT_FLAG_LAST_KNOWN_GOOD  (1ULL << 5)
#define BOOT_FLAG_SHOW_PROGRESS    (1ULL << 6)
#define BOOT_FLAG_INSTALLER        (1ULL << 7)
#define BOOT_FLAG_LIVE_ROOT        (1ULL << 8)

#define BOOT_CONFIG_INIT_MAX 256  /* PID1 init path buffer */

typedef struct
{
    MEMORY_MAP MemoryMap;

    UINT64 FADT;
    UINT64 MADT;
    UINT64 HPET;
    UINT64 MCFG;

    // Preallocated AP stacks used before the kernel memory allocator is available.
    UINT64 *saved_mtrrs;
    void   *temp_stack[MAX_CPU_NUM];

    int is_qemu;

    UINT64 boot_flags;

    UINT64 installer_root_pak;
    UINT64 installer_root_pak_size;
    UINT64 system_payload_pak;
    UINT64 system_payload_pak_size;

    char init[BOOT_CONFIG_INIT_MAX]; /* PID1 path: from boot.conf */
} BOOT_CONFIG;

#endif
