from numbapro import cuda
import support
from timeit import default_timer as timer
import numpy as np
import unittest

REPEAT = 25

class TestPinned(support.CudaTestCase):

    def _template(self, name, A):
        A0 = np.copy(A)

        s = timer()
        stream = cuda.stream()
        ptr = cuda.to_device(A, copy=False, stream=stream)

        ptr.to_device(stream=stream)

        ptr.to_host(stream=stream)
        stream.synchronize()

        e = timer()

        self.assertTrue(np.allclose(A, A0))

        elapsed = e - s
        return elapsed

    def test_pinned(self):
        A = np.arange(2*1024*1024) # 16 MB
        total = 0
        with cuda.pagelock(A):
            for i in range(REPEAT):
                total += self._template('pinned', A)
        print 'pinned', total / REPEAT

    def test_unpinned(self):
        A = np.arange(2*1024*1024) # 16 MB
        total = 0
        for i in range(REPEAT):
            total += self._template('unpinned', A)
        print 'unpinned', total / REPEAT


if __name__ == '__main__':
    unittest.main()

