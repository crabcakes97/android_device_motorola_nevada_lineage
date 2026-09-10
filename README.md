# LineageOS device tree — Motorola Nevada (moto g play 2026, XT2615-1)

Bring-up of LineageOS 23 (Android 16, BP2A release) for the Motorola Nevada —
moto g play 2026 — MediaTek MT6835 (Dimensity 6300), RETUS variant.

## Stock baseline (everything here matches it)

- Stock build: **W1WNS36.18-114-1** (RETUS, XT2615-1)
- Firmware used for all blobs, kernel and verified values:
  `XT2615-1_NEVADA_RETUS_16_W1WNS36.18-114-1_..._CFC.xml.zip`
- Partitions in super (verified from LP table — **no odm partition**):
  `product_a, system_a, system_dlkm_a, system_ext_a, vendor_a, vendor_dlkm_a`

## Layout

```
device/motorola/nevada/          # device tree (BoardConfig, device.mk, HAL sources,
                                 #   init, configs, sepolicy, overlays, extract scripts)
device/motorola/nevada-kernel/   # prebuilt stock kernel: Image.gz, dtb, 196 vendor
                                 #   + 197 ramdisk modules (carved from stock)
vendor/motorola/nevada/          # generated makefiles (Android.bp/.mk) + blob lists.
                                 #   extracted binaries live in proprietary/ + radio/
                                 #   (NOT in git — regenerate, see below)
```

## Current strategy: prebuilt kernel (deliberate)

`TARGET_FORCE_PREBUILT_KERNEL := true`. The 393 stock `.ko` files only load on the
stock kernel they were built against, so first boot uses the carved stock kernel.
Source kernel (`MotorolaMobilityLLC/kernel-mtk`,
branch `android-16-release-w1wn36.18-114` — same release tag as stock) plus the
matching `motorola-kernel-modules` branch is the planned second step.

## Regenerating blobs

```bash
# from a Lineage 23 checkout with this tree at device/motorola/nevada:
cd device/motorola/nevada
PYTHONPATH=../../../tools/extract-utils python3 extract-files.py /path/to/dump
# regenerates vendor/motorola/nevada makefiles + pulls proprietary/ + radio/
```

`proprietary-files.txt` documents every deviation from a naive pull (dangling
stock symlinks, platform-duplicated libs, AIDL-version fixups — each verified
against the dump with readelf). `extract-files.py` carries the matching blob
fixups (libutils-v32, shims, NDK repoints).

## Build

```bash
source build/envsetup.sh
lunch lineage_nevada-bp2a-userdebug   # bp2a, not ap4a (platform BUILD_ID is BP2A)
mka bacon                             # produces the TWRP-flashable zip + recovery
```

Requires the MTK dependency projects (see manifest): `hardware/mediatek`,
`device/mediatek/sepolicy_vndr`, `hardware/motorola`, `vendor/mediatek/ims`.

## Status

First bringup in progress: tree parses, lunch succeeds, full build underway.
Expected first-boot risks are SELinux policy (boots enforcing) and HAL
compatibility shims — standard bringup follow-ups, see tree NOTEs.
