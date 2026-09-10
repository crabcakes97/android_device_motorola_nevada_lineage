# LineageOS Device Tree for Motorola Moto G Play 2026 (nevada)

| Basic                   | Spec Sheet |
| -----------------------:|:-----------|
| CPU                     | Octa-core (2x Cortex-A76 + 6x Cortex-A55) |
| Chipset                 | MediaTek Dimensity 6300 / MT6835 (6 nm) |
| GPU                     | ARM Mali-G57 MC2 |
| Memory                  | 4 GB RAM, 64 GB UFS 2.2, microSD up to 1 TB |
| Shipped Android Version | 16 (W1WNS36.18-114-1 RETUS, XT2615-1) |
| Battery                 | 5200 mAh, 18W charging |
| Display                 | 6.7" HD+ (720x1604), 260 dpi |
| Fingerprint             | Side-mounted (Goodix + FPC 2.1 services) |
| Kernel                  | 5.15 (GKI android13-5.15) + Motorola MTK vendor, DTS `mt6835-nevada-*` |

Codename: `nevada`. Model: `XT2615-1` (RETUS). SoC: `mt6835`. Lineage 23 / Android 16 (BP2A).

## Repo layout (standard device-tree root)

```text
BoardConfig.mk  device.mk  lineage_nevada.mk  extract-files.py  ...
audio/  configs/  init/  overlay/  sepolicy/  lights/  power/
vibrator/  sensors/  fingerprint-egis/  fingerprint-gdx/  libshims/
props/  proprietary-files.txt  proprietary-firmware.txt
kernel/    # prebuilt stock kernel: Image.gz, dtb/, vendor/*.ko (196),
           #   vendor_ramdisk/*.ko (197), modules.load.*
vendor/    # generated makefiles (Android.bp/.mk); extracted binaries live in
           #   vendor/proprietary/ + vendor/radio/ (NOT in git — regenerate below)
```

## Stock baseline (everything here matches it)

- Stock build: **W1WNS36.18-114-1** (RETUS, XT2615-1)
- Firmware: `XT2615-1_NEVADA_RETUS_16_W1WNS36.18-114-1_..._CFC.xml.zip`
- Super partitions (verified from LP table — **no odm partition**):
  `product_a, system_a, system_dlkm_a, system_ext_a, vendor_a, vendor_dlkm_a`
- Partition sizes from RETUS PGPT; fingerprints/security patch (2026-04-01)
  from stock build props; kernel/DTB/modules carved from stock images.

## Regenerating blobs

```bash
# from a Lineage 23 checkout with this tree at device/motorola/nevada:
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
mka bacon                             # TWRP-flashable zip + recovery
```

Requires the MTK dependency projects: `hardware/mediatek`,
`device/mediatek/sepolicy_vndr`, `hardware/motorola`, `vendor/mediatek/ims`.
Power HAL is source-built (Pixel power HAL + mtkpower stub); Bluetooth,
fingerprint (Goodix/FPC), GNSS and camera run stock services.

## Kernel source (second step, after first boot)

Prebuilt stock kernel is used deliberately for bringup (`TARGET_FORCE_PREBUILT_KERNEL`).
Source: `MotorolaMobilityLLC/kernel-mtk`, branch `android-16-release-w1wn36.18-114`
(same release tag as stock) + matching `motorola-kernel-modules` branch.
DTS overlays: `mt6835-nevada-common-overlay.dtsi`, `mt6835-nevada-evb-overlay.dts`.
