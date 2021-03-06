import argparse
import os
import unittest
import tempfile

from ast2vec.coocc import Cooccurrences
from ast2vec.model2.prox import prox_entry
from ast2vec.model2.proxbase import EDGE_TYPES
import ast2vec.tests.models as paths


class ProxTests(unittest.TestCase):
    def test_prox(self):
        with tempfile.TemporaryDirectory(prefix="ast2vec-test-source2bow-") as tmpdir:
            args = argparse.Namespace(processes=1, input=os.path.dirname(__file__),
                                      output=tmpdir, matrix_type="Swivel", filter=paths.UAST,
                                      edges=EDGE_TYPES, overwrite_existing=True)
            prox_entry(args)
            prox = Cooccurrences().load(os.path.join(tmpdir, os.listdir(tmpdir)[0]))
        self.assertIn("pickle", prox.tokens)
        self.assertIn("setuptool", prox.tokens)
        self.assertIn("try", prox.tokens)
        self.assertIn("RoleId_103", prox.tokens)
        self.assertIn("RoleId_73", prox.tokens)
        self.assertEqual(prox.matrix.shape, (543, 543))
        self.assertEqual(prox.matrix.nnz, 14819)


if __name__ == "__main__":
    unittest.main()
