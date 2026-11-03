import hashlib
import tempfile
import unittest
from pathlib import Path

from scripts.write_data_manifest import write_manifest


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

    def test_empty_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            data_dir = Path(temporary_directory) / "data"
            data_dir.mkdir()

            with self.assertRaisesRegex(ValueError, "No files found"):
                write_manifest(data_dir, data_dir.parent / "manifest.sha256")


if __name__ == "__main__":
    unittest.main()
