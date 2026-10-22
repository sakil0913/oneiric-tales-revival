# -*- coding: utf-8 -*-
"""快速鉴定一个《梦界物语》APK 的版本与内容规模。

用法:
    python check_apk.py <apk路径> [另一个apk路径 ...]

输出: 版本号、数据文件数、il2cpp 元数据版本、TextAsset/纹理数量、与基线(1.0)的差异。
"""
import hashlib
import os
import sys
import zipfile

BASELINE = {
    "size": 68524163,
    "versionName": "1.0",
    "versionCode": "12786",
    "data_files": 2185,
    "metadata_ver": 22,
    "unity": "5.5.0p4",
}


def sha256(path, limit=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def manifest_info(apk):
    """Return (package, versionName, versionCode, minSdk, targetSdk)."""
    try:
        from pyaxmlparser import APK
        a = APK(apk)
        return (a.package, a.version_name, str(a.version_code),
                a.get_min_sdk_version(), a.get_target_sdk_version())
    except Exception:
        return ("?", "?", "?", "?", "?")


def unity_version(z):
    """unity version string lives right after the SerializedFile header of globalgamemanagers."""
    try:
        with z.open("assets/bin/Data/globalgamemanagers") as f:
            head = f.read(64)
        idx = head.find(b"5.")
        if idx > 0:
            end = head.find(b"\x00", idx)
            return head[idx:end].decode("ascii", "replace")
    except Exception:
        pass
    return "?"


def inspect(apk):
    size = os.path.getsize(apk)
    pkg, vname, vcode, minsdk, targetsdk = manifest_info(apk)
    with zipfile.ZipFile(apk) as z:
        names = z.namelist()
        data = [n for n in names if n.startswith("assets/bin/Data/") and "/" not in n[len("assets/bin/Data/"):]]
        hash_named = [n for n in data if len(os.path.basename(n)) == 32]
        has_managed = any(n.endswith("Assembly-CSharp.dll") for n in names)
        meta = "assets/bin/Data/Managed/Metadata/global-metadata.dat"
        meta_size = z.getinfo(meta).file_size if meta in names else 0
        uver = unity_version(z)
        dex = [n for n in names if n.startswith("classes") and n.endswith(".dex")]
        so = [n for n in names if n.endswith("libil2cpp.so")]

    print("=" * 72)
    print("文件:", apk)
    print("大小: {:,} 字节 ({:.1f} MiB)".format(size, size / 1048576))
    print("sha256:", sha256(apk))
    print("包名:", pkg, "| versionName:", vname, "| versionCode:", vcode)
    print("SDK:", minsdk, "->", targetsdk)
    print("Unity:", uver, "| 数据文件: {:,} (其中哈希名 {:,})".format(len(data), len(hash_named)))
    print("global-metadata: {:,} 字节 | dex: {} | libil2cpp: {}".format(meta_size, len(dex), len(so)))
    print("Mono 程序集(应为 0，il2cpp 构建):", 1 if has_managed else 0)

    same = size == BASELINE["size"]
    print("-" * 72)
    if same:
        print("判定: 与基线 1.0 完全同尺寸 —— 是同一份包（极可能就是你已有的那份）")
    elif vcode != "?" and vcode.isdigit() and int(vcode) > int(BASELINE["versionCode"]):
        print("判定: 比基线(12786) 新 —— versionCode {}, 值得深入分析".format(vcode))
    else:
        print("判定: 与基线不同，需人工比对（尺寸/版本号/数据文件数）")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for p in sys.argv[1:]:
        if os.path.isfile(p):
            inspect(p)
        else:
            print("跳过（不存在）:", p)
