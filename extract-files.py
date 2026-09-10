#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Nevada (moto g play 2026, XT2615-1, MT6835) blob fixups.
# Every path below was verified present in the RETUS W1WNS36.18-114-1
# super dump. Blob NEEDED tables were inspected with readelf:
# stock links unversioned libutils/libalsautils, hence the -v32/-v31
# replacements; libcam.hal3a references SetTaskProfiles (provided by
# hardware/lineage/compat libprocessgroup_shim); the Goodix HAL needs
# newer Moto fingerprint symbols (libshim_fp in device libshims/).
# AIDL-version dupes rejected by Soong are handled by dropping spurious
# versioned NEEDEDs (verified symbol-free) or repointing V3->V6 where the
# frozen snapshots are ABI-identical.
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/nevada',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/motorola',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('vendor.mediatek.hardware.videotelephony@1.0',): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc': blob_fixup()
        .regex_replace('start', 'enable'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    ('vendor/bin/hw/android.hardware.gnss-service.mediatek', 'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    ('vendor/bin/mnld', 'vendor/lib64/hw/android.hardware.sensors@2.X-subhal-mediatek.so', 'vendor/lib64/mt6835/libcam.utils.sensorprovider.so'): blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/hw/mt6835/vendor.mediatek.hardware.pq_aidl-impl.so': blob_fixup()
        .add_needed('android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libalsautils.so', 'libalsautils-v31.so'),
    ('vendor/lib64/mt6835/libcam.hal3a.v3.so', 'vendor/lib64/hw/hwcomposer.mtk_common.so'): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    ('vendor/lib64/mt6835/libneuralnetworks_sl_driver_mtk_prebuilt.so', 'vendor/lib64/libstfactory-vendor.so',
     'vendor/lib64/libnvram.so', 'vendor/lib64/libsysenv.so', 'vendor/lib64/libtflite_mtk.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so', 'vendor/lib64/mt6835/libmtkcam_stdutils.so',
     'vendor/lib64/sensors.moto.so'): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('libbase_shim.so'),
    'vendor/etc/vintf/manifest/manifest_media_c2_V1_1_atom_only.xml': blob_fixup()
        .regex_replace('1.1', '1.2')
        .regex_replace('@1.0', '@1.2')
        .regex_replace('default9', 'default'),
    ('vendor/lib64/mt6835/lib3a.flash.so', 'vendor/lib64/mt6835/lib3a.ae.stat.so',
     'vendor/lib64/mt6835/lib3a.sensors.flicker.so', 'vendor/lib64/mt6835/lib3a.sensors.color.so'): blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/mt6835/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    # Goodix HAL uses newer Moto fingerprint methods; source-built moto lib
    # lacks them, so inject libshim_fp stubs (blob itself comes from source).
    'vendor/lib64/libgoodixhwfingerprint.so': blob_fixup()
        .add_needed('libshim_fp.so'),
    'vendor/bin/hw/android.hardware.security.keymint@2.0-service.trustonic': blob_fixup()
        .add_needed('android.hardware.security.rkp-V1-ndk.so')
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('android.hardware.security.keymint-V1-ndk_platform.so', 'android.hardware.security.keymint-V1-ndk.so')
        .replace_needed('android.hardware.security.sharedsecret-V1-ndk_platform.so', 'android.hardware.security.sharedsecret-V1-ndk.so')
        .replace_needed('android.hardware.security.secureclock-V1-ndk_platform.so', 'android.hardware.security.secureclock-V1-ndk.so'),
    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),
    # libtpa DT_NEEDEDs keymint-V2-ndk but references no V2 symbols; its
    # keymint refs are V1-namespace (fromBinder etc.), provided by platform
    # V1 (single installer, no blob). libkeymint.so (HIDL) is also unused
    # (0 HIDL-named UND refs of 164) and only drags keymint-V4 into the
    # closure (dup rule), so it goes too. IRemotelyProvisionedComponent is
    # an RKP (not keymint) interface — platform rkp-V3 exports it. V2 stays
    # stripped.
    'vendor/lib64/libtpa.so': blob_fixup()
        .remove_needed('android.hardware.security.keymint-V2-ndk.so')
        .remove_needed('libkeymint.so')
        .add_needed('android.hardware.security.keymint-V1-ndk.so')
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    # librilfusion DT_NEEDEDs radio sim/config-V2-ndk but references no V2
    # symbols (uses V1 AIDL + HIDL). Both V1 libs resolve to platform copies
    # (frozen V1 API carries the symbols). V2 stays stripped (Soong dup rule).
    'vendor/lib64/librilfusion.so': blob_fixup()
        .remove_needed('android.hardware.radio.sim-V2-ndk.so')
        .remove_needed('android.hardware.radio.config-V2-ndk.so')
        .add_needed('android.hardware.radio.sim-V1-ndk.so')
        .add_needed('android.hardware.radio.config-V1-ndk.so'),
    # pq_aidl V1-ndk DT_NEEDEDs graphics.common-V3-ndk for HardwareBuffer
    # parcel methods; V3 and V6 snapshots differ only in comments (same ABI),
    # so repoint at V6 (platform gralloctypes uses V6; Soong rejects both).
    'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V1-ndk.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V6-ndk.so'),
    # Codec2 VPP AI plugins DT_NEED graphics.allocator-V1-ndk but reference no
    # allocator AIDL symbols; V2 arrives via the codec2 stack. (Their one
    # graphics.common ref is HIDL-era GraphicBufferMapper, so V3-ndk is
    # spurious too while platform gralloctypes uses V6.)
    'vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so': blob_fixup()
        .remove_needed('android.hardware.graphics.allocator-V1-ndk.so')
        .remove_needed('android.hardware.graphics.common-V3-ndk.so'),
    'vendor/lib64/libcodec2_vpp_AISR_plugin.so': blob_fixup()
        .remove_needed('android.hardware.graphics.allocator-V1-ndk.so')
        .remove_needed('android.hardware.graphics.common-V3-ndk.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'nevada',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
