import hashlib
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

from .constants import TOOLCHAIN, TOOLCHAIN_VERSION, DEPENDENCIES, BUFFER_SIZE

RELEASE_URL = f"https://github.com/farhaanaliii/kosei-toolchain/releases/download/{TOOLCHAIN_VERSION}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def download_file(url: str, destination: Path) -> bool:
    try:
        with urllib.request.urlopen(url) as resp, destination.open("wb") as out:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            while chunk := resp.read(BUFFER_SIZE):
                out.write(chunk)
                downloaded += len(chunk)
                if total > 0:
                    percent = int(downloaded * 100 / total)
                    print(f"\r[*] downloading {destination.name}: {percent}%", end="", flush=True)
            print()
        return True
    except Exception as e:
        print(f"\n[-] download failed: {e}")
        destination.unlink(missing_ok=True)
        return False


def fetch_checksums() -> dict[str, str]:
    try:
        with urllib.request.urlopen(f"{RELEASE_URL}/checksums.sha256") as resp:
            content = resp.read().decode("utf-8")
        checksums = {}
        for line in content.splitlines():
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                checksums[Path(parts[1].strip()).name] = parts[0]
        return checksums
    except Exception as e:
        print(f"[-] failed to fetch checksums: {e}")
    return {}


def safe_extract(tar: tarfile.TarFile, target_dir: Path) -> bool:
    base = target_dir.resolve()
    for member in tar.getmembers():
        dest = (base / member.name).resolve()
        if base not in dest.parents and dest != base:
            return False
    if hasattr(tarfile, "data_filter"):
        tar.extractall(base, filter="data")
    else:
        tar.extractall(base)
    return True


def setup_toolchain(force: bool = False) -> bool:
    missing = list(DEPENDENCIES) if force else [name for name in DEPENDENCIES if not (TOOLCHAIN / name).exists()]
    if not missing:
        print(f"[*] toolchain already installed in {TOOLCHAIN}")
        return True

    checksums = fetch_checksums()
    if not checksums:
        return False

    TOOLCHAIN.mkdir(parents=True, exist_ok=True)

    if force or len(missing) == len(DEPENDENCIES):
        expected_hash = checksums.get("toolchain.tar.gz")
        if not expected_hash:
            print("[-] checksum for toolchain.tar.gz unavailable")
            return False

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            archive = tmp_dir / "toolchain.tar.gz"
            extract_dir = tmp_dir / "extracted"
            extract_dir.mkdir()

            if not download_file(f"{RELEASE_URL}/toolchain.tar.gz", archive):
                return False

            if sha256(archive) != expected_hash:
                print("[-] checksum mismatch for toolchain.tar.gz")
                return False

            print("[*] extracting toolchain")
            with tarfile.open(archive, "r:gz") as tar:
                if not safe_extract(tar, extract_dir):
                    print("[-] unsafe archive paths detected")
                    return False

            if not all((extract_dir / name).exists() for name in DEPENDENCIES):
                print("[-] toolchain bundle missing required dependencies")
                return False

            for item in extract_dir.iterdir():
                dest = TOOLCHAIN / item.name
                if dest.is_dir():
                    shutil.rmtree(dest, ignore_errors=True)
                item.replace(dest)

        print(f"[*] toolchain ready in {TOOLCHAIN}")
        return True

    for filename in missing:
        expected_hash = checksums.get(filename)
        if not expected_hash:
            print(f"[-] checksum for {filename} unavailable")
            return False

        target_path = TOOLCHAIN / filename
        temp_target = TOOLCHAIN / f".{filename}.tmp"

        if not download_file(f"{RELEASE_URL}/{filename}", temp_target):
            return False

        if sha256(temp_target) != expected_hash:
            print(f"[-] checksum mismatch for {filename}")
            temp_target.unlink(missing_ok=True)
            return False

        temp_target.replace(target_path)

    print(f"[*] toolchain updated in {TOOLCHAIN}")
    return True


def ensure_dependencies() -> bool:
    missing = [name for name in DEPENDENCIES if not (TOOLCHAIN / name).exists()]
    if not missing:
        return True
    print(f"[*] missing toolchain in {TOOLCHAIN}: {', '.join(missing)}")
    print("[*] run 'kosei setup' to install the toolchain")
    return False
