# Prebuilt kernel directory for nevada (Lineage 23 bringup).
#
# SEEDED FROM STOCK FIRMWARE
# (XT2615-1_NEVADA_RETUS_16_W1WNS36.18-114-1):
#   Image.gz                  <- carved from boot.img (boot v4, gzip, 21.5 MB)
#   dtb/nevada.dtb            <- carved from vendor_boot.img DT table (1 entry)
#   vendor_ramdisk/*.ko       <- 197 modules from vendor_boot vendor_ramdisk
#   modules.load.vendor_ramdisk / modules.load.recovery <- from vendor_ramdisk
#
# STILL NEEDED (from super.img -> vendor_dlkm, requires lpunpack):
#   vendor/*.ko
#   modules.load.vendor
#   headers/  (or point TARGET_KERNEL_SOURCE at kernel-mtk source instead)
#
# Proper long-term source: kernel-mtk
# (https://github.com/MotorolaMobilityLLC/kernel-mtk,
#  branch android-16-release-w1wn36.18-114,
#  config build.config.mtk.aarch64, DTS mt6835-nevada-evb-overlay).
# Build it and refresh this directory, or switch BoardConfig.mk off
# TARGET_FORCE_PREBUILT_KERNEL once source-built kernel + modules are ready.
