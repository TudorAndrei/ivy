# global
import math
import jax.numpy as jnp
from typing import Union, Tuple, Optional, List
from numbers import Number

# local
from ivy.functional.backends.jax import JaxArray
import ivy


def roll(x: JaxArray,
         shift: Union[int, Tuple[int, ...]],
         axis: Optional[Union[int, Tuple[int, ...]]] = None,
         out: Optional[JaxArray] = None) \
        -> JaxArray:
    ret = jnp.roll(x, shift, axis)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def squeeze(x: JaxArray,
            axis: Union[int, Tuple[int], List[int]] = None,
            out: Optional[JaxArray] = None)\
        -> JaxArray:
    if x.shape == ():
        if axis is None or axis == 0 or axis == -1:
            ret = x
        raise ValueError('tried to squeeze a zero-dimensional input by axis {}'.format(axis))
    else:
        ret = jnp.squeeze(x, axis)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def _flat_array_to_1_dim_array(x):
    return x.reshape((1,)) if x.shape == () else x


# noinspection PyShadowingBuiltins
def flip(x: JaxArray,
         axis: Optional[Union[int, Tuple[int], List[int]]] = None,
         out: Optional[JaxArray] = None)\
         -> JaxArray:
    ret = jnp.flip(x, axis=axis)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def expand_dims(x: JaxArray,
                axis: int = 0,
                out: Optional[JaxArray] = None) \
        -> JaxArray:
    try:
        ret = jnp.expand_dims(x, axis)
        if ivy.exists(out):
            return ivy.inplace_update(out, ret)
        return ret
    except ValueError as error:
        raise IndexError(error)


def stack(x: Union[Tuple[JaxArray], List[JaxArray]],
          axis: Optional[int] = None,
          out: Optional[JaxArray] = None) \
        -> JaxArray:
    if axis is None:
        axis = 0
    ret = jnp.stack(x, axis=axis)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def permute_dims(x: JaxArray,
                axes: Tuple[int,...],
                 out: Optional[JaxArray] = None) \
        -> JaxArray:
    ret = jnp.transpose(x,axes)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def reshape(x: JaxArray,
            shape: Tuple[int, ...],
            copy: Optional[bool] = None,
            out: Optional[JaxArray] = None)\
        -> JaxArray:
    ret = jnp.reshape(x, shape)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def concat(xs: List[JaxArray], axis: int = 0,
           out: Optional[JaxArray] = None) -> JaxArray:
    is_tuple = type(xs) is tuple

    if axis==None:
        if is_tuple:
            xs = list(xs)
        for i in range(len(xs)):
            if xs[i].shape ==():
                xs[i] = jnp.ravel(xs[i])
        if is_tuple:
            xs = tuple(xs)

    ret = jnp.concatenate(xs, axis)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


# Extra #
# ------#


def split(x, num_or_size_splits=None, axis=0, with_remainder=False):
    if x.shape == ():
        if num_or_size_splits is not None and num_or_size_splits != 1:
            raise Exception('input array had no shape, but num_sections specified was {}'.format(num_or_size_splits))
        return [x]
    if num_or_size_splits is None:
        num_or_size_splits = x.shape[axis]
    elif isinstance(num_or_size_splits, int) and with_remainder:
        num_chunks = x.shape[axis] / num_or_size_splits
        num_chunks_int = math.floor(num_chunks)
        remainder = num_chunks - num_chunks_int
        if remainder != 0:
            num_or_size_splits = [num_or_size_splits] * num_chunks_int + [int(remainder * num_or_size_splits)]
    if isinstance(num_or_size_splits, (list, tuple)):
        num_or_size_splits = jnp.cumsum(jnp.array(num_or_size_splits[:-1]))
    return jnp.split(x, num_or_size_splits, axis)


def repeat(x: JaxArray,
           repeats: Union[int, List[int]],
           axis: int = None,
           out: Optional[JaxArray] = None)\
        -> JaxArray:
    ret = jnp.repeat(x, repeats, axis)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def tile(x: JaxArray,
         reps,
         out: Optional[JaxArray] = None)\
        -> JaxArray:
    ret = jnp.tile(x, reps)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def clip(x, x_min, x_max, out: Optional[JaxArray] = None):
    ret = jnp.clip(x, x_min, x_max)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def constant_pad(x: JaxArray,
                 pad_width: List[List[int]],
                 value: Number = 0.,
                 out: Optional[JaxArray] = None)\
        -> JaxArray:
    ret = jnp.pad(_flat_array_to_1_dim_array(x), pad_width, constant_values=value)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def zero_pad(x: JaxArray,
             pad_width: List[List[int]],
             out: Optional[JaxArray] = None):
    ret = jnp.pad(_flat_array_to_1_dim_array(x), pad_width, constant_values=0)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret


def swapaxes(x: JaxArray,
             axis0: int,
             axis1: int,
             out: Optional[JaxArray] = None)\
        -> JaxArray:
    ret = jnp.swapaxes(x, axis0, axis1)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret)
    return ret
