import jax.numpy as jnp
from jax import jit, device_put
from jax import random
import numpy as np
import time


def global_int(x, w):
    z = x[:,1] + w
    t = z - w
    return t

if __name__ == "__main__":
    M = 256
    N = 4
    K = 9
    P = 1

    # global int
    x = np.random.randn(M,N).astype(np.float32)
    w = np.random.randn(M).astype(np.float32)
    x = device_put(x)
    w = device_put(w)

    sargs = [x, w]
    fast_func = jit(global_int)

    time1 = time.time()
    for i in range(1000):
        global_int(*sargs).block_until_ready()
    time2 = time.time()

    print("jax gpu time: ", time2 - time1)

    time1 = time.time()
    for i in range(1000):
        fast_func(*sargs).block_until_ready()
    time2 = time.time()

    print("jax jit time: ", time2 - time1)
