import base64
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest

from geocities_rebuild.__main__ import InputError, inventory, main, source_directory
from scripts.create_fixture import create_fixture


class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = create_fixture(self.base / "source")

    def test_inventory_preserves_case_and_detects_collisions(self):
        original = (self.source / "Home" / "INDEX.HTML").read_bytes()
        result = inventory(source_directory(str(self.source)))
        self.assertEqual(result["entry_count"], 9)
        self.assertIn(["Home", "home"], result["casefold_collisions"])
        self.assertIn(
            ["Home/INDEX.HTML", "home/index.html"],
            result["casefold_collisions"],
        )
        self.assertEqual((self.source / "Home" / "INDEX.HTML").read_bytes(), original)
        paths = [record["path"] for record in result["entries"]]
        self.assertIn("Home/odd?name.html", paths)
        self.assertIn("Home/line\nbreak.txt", paths)

    def test_symlink_not_followed(self):
        result = inventory(self.source)
        links = [record for record in result["entries"] if record["type"] == "symlink"]
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["path"], "loop")
        self.assertEqual(base64.b64decode(links[0]["target_bytes_base64"]), b".")

    def test_cap_stops_scanning(self):
        with self.assertRaises(InputError):
            inventory(self.source, max_entries=2)

    def test_manifest_is_new_and_outside_source(self):
        output = self.base / "manifest.json"
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["scan", "--source", str(self.source), "--output", str(output)]), 0)
            self.assertEqual(main(["scan", "--source", str(self.source), "--output", str(output)]), 2)
            self.assertEqual(
                main(["scan", "--source", str(self.source), "--output", str(self.source / "no.json")]),
                2,
            )
        manifest = json.loads(output.read_text())
        self.assertEqual(manifest["entry_count"], 9)
        self.assertFalse((self.source / "no.json").exists())

    def test_source_root_is_not_allowed(self):
        with self.assertRaises(InputError):
            source_directory("/")

    def test_preflight_requires_separated_paths(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["preflight", "--source", str(self.source)]), 0)
            self.assertEqual(
                main(["preflight", "--source", str(self.source), "--work", str(self.source / "work")]),
                2,
            )

    @unittest.skipUnless(os.name == "posix", "Requires a POSIX filesystem")
    def test_raw_filename_roundtrip(self):
        name = b"raw-\xff.html"
        fd = os.open(os.fsencode(self.source) + b"/" + name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
        result = inventory(self.source)
        raw = {base64.b64decode(item["path_bytes_base64"]) for item in result["entries"]}
        self.assertIn(name, raw)

    def test_fixture_refuses_overwrite(self):
        with self.assertRaises(FileExistsError):
            create_fixture(self.source)


if __name__ == "__main__":
    unittest.main()
