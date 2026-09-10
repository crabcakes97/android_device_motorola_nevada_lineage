#
# SPDX-FileCopyrightText: LineageOS
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/motorola/nevada/device.mk)

# Inherit some common lineageOS stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

TARGET_BOOT_ANIMATION_RES := 720

PRODUCT_NAME := lineage_nevada
PRODUCT_DEVICE := nevada
PRODUCT_MANUFACTURER := Motorola
PRODUCT_BRAND := motorola
PRODUCT_MODEL := moto g play - 2026

PRODUCT_GMS_CLIENTID_BASE := android-motorola

# Stock values from system/build.prop (RETUS W1WNS36.18-114-1 super image):
#   ro.system.build.fingerprint=motorola/nevada_g_sys/nevada:16/W1WNS36M.18-114-1/cca41:user/release-keys
#   ro.product.system.model=moto g play - 2026
PRODUCT_BUILD_PROP_OVERRIDES += \
    DeviceName=nevada \
    BuildDesc="nevada_g_sys-user 16 W1WNS36M.18-114-1 cca41 release-keys" \
    BuildFingerprint=motorola/nevada_g_sys/nevada:16/W1WNS36M.18-114-1/cca41:user/release-keys
