import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.write_data_manifest import verify_manifest, write_manifest


class WriteDataManifestTests(unittest.TestCase):
    def test_manifest_is_sorted_and_uses_relative_posix_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            data_dir = root / "data"
            (data_dir / "nested").mkdir(parents=True)
            (data_dir / "z.csv").write_bytes(b"z\n")
            (data_dir / "nested" / "a.csv").write_bytes(b"a\n")
            output = root / "data-manifest.sha256"

            count = write_manifest(data_dir, output)

            expected = [
                f"{hashlib.sha256(b'a\n').hexdigest()}  nested/a.csv",
                f"{hashlib.sha256(b'z\n').hexdigest()}  z.csv",
            ]
            self.assertEqual(count, 2)
            self.assertEqual(output.read_text(encoding="utf-8").splitlines(), expected)

    def test_manifest_verification_detects_changed_data(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            data_dir = root / "data"
            data_dir.mkdir()
            data_file = data_dir / "train.csv"
            data_file.write_bytes(b"original\n")
            manifest = root / "data-manifest.sha256"

            write_manifest(data_dir, manifest)
            self.assertEqual(verify_manifest(data_dir, manifest), 1)

            data_file.write_bytes(b"changed\n")
            with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                verify_manifest(data_dir, manifest)

    def test_manifest_rejects_paths_outside_data_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            data_dir = root / "data"
            data_dir.mkdir()
            outside = root / "outside.csv"
            outside.write_bytes(b"outside\n")
            manifest = root / "data-manifest.sha256"
            manifest.write_text(
                f"{hashlib.sha256(b'outside\n').hexdigest()}  ../outside.csv\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "escapes the data directory"):
                verify_manifest(data_dir, manifest)

    def test_empty_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            data_dir = Path(temporary_directory) / "data"
            data_dir.mkdir()

            with self.assertRaisesRegex(ValueError, "No files found"):
                write_manifest(data_dir, data_dir.parent / "manifest.sha256")


if __name__ == "__main__":
    unittest.main()
