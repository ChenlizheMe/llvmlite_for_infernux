"""Source-side release metadata tests; no LLVM build is required."""

import importlib.util
from pathlib import Path
import unittest

from packaging.version import Version


ROOT = Path(__file__).resolve().parents[1]


def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VersionTests(unittest.TestCase):
    def test_runtime_version_file_matches_the_generator(self):
        versioneer = load_file("fork_versioneer", ROOT / "versioneer.py")
        generated = versioneer.LONG_VERSION_PY["git"] % {
            "DOLLAR": "$", "TAG_PREFIX": "v", "PARENTDIR_PREFIX": "llvmlite-",
            "VERSIONFILE_SOURCE": "llvmlite/_version.py",
        }
        self.assertEqual((ROOT / "llvmlite/_version.py").read_text().strip(),
                         generated.strip())

    def test_local_tags_remain_pep440_in_source_and_generated_versions(self):
        versioneer = load_file("fork_versioneer", ROOT / "versioneer.py")
        generated = {}
        exec(versioneer.LONG_VERSION_PY["git"] % {
            "DOLLAR": "$",
            "TAG_PREFIX": "v", "PARENTDIR_PREFIX": "llvmlite-",
            "VERSIONFILE_SOURCE": "llvmlite/_version.py",
        }, generated)
        cases = (
            ("v0.49.0-0-gabc123", "0.49.0", False),
            ("v0.49.0-2-gabc123", "0.49.0+2.gabc123", False),
            ("v0.49.0-0-gabc123-dirty", "0.49.0+0.gabc123.dirty", True),
            ("v0.49.0+infernux.4-0-gabc123", "0.49.0+infernux.4", False),
            ("v0.49.0+infernux.4-2-gabc123", "0.49.0+infernux.4.2.gabc123", False),
            ("v0.49.0+infernux.4-0-gabc123-dirty",
             "0.49.0+infernux.4.0.gabc123.dirty", True),
        )
        source = load_file("fork_source_version", ROOT / "llvmlite/_version.py")
        parsers = (versioneer.git_parse_vcs_describe,
                   generated["git_parse_vcs_describe"],
                   source.git_parse_vcs_describe)
        for parser in parsers:
            for description, expected, dirty in cases:
                with self.subTest(parser=parser.__module__, description=description):
                    actual, actual_dirty = parser(description, "v", False)
                    self.assertEqual(actual, expected)
                    self.assertEqual(actual_dirty, dirty)
                    self.assertEqual(str(Version(actual)), actual)


if __name__ == "__main__":
    unittest.main()
