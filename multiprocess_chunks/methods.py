'''
Chunk-based, multiprocess processing of iterables.
Uses the `multiprocess` package to perform the multiprocessization.
Uses the `cloudpickle` to pickle hard-to-pickle objects.
'''

from math import ceil
import cloudpickle
from pathos.multiprocessing import cpu_count
from pathos.multiprocessing import ProcessPool as Pool


def map_list_as_chunks(l, f, extra_data, cpus=None, max_chunk_size=None):
    '''
    A wrapper around `pathos.multiprocessing.ProcessPool.uimap` that processes a list in chunks.
    Differs from `map_list_in_chunks` in that this method calls `f` once for each chunk.

    uimap already chunks but if you have extra data to pass in it will pickle
    it for every item. This function passes in the extra data to each chunk
    which significantly saves on pickling.
    https://stackoverflow.com/questions/53604048/iterating-the-results-of-a-multiprocessing-list-is-consuming-large-amounts-of-me

    Parameters
    ----------
    l : list
      the list
    f : function
      the function to process each item
      takes two parameters: chunk, extra_data
    extra_data : object
      the extra data to pass to each f
    cpus : int
      the number of cores to use to split the chunks across
    max_chunk_size : int
      the maximum size for each chunk
    '''
    cpus = cpu_count() if cpus is None else cpus
    max_chunk_size = float('inf') if max_chunk_size is None else max_chunk_size
    chunk_length = min(max_chunk_size, max(1, ceil(len(l) / cpus)))
    chunks = [l[x:x+chunk_length] for x in range(0, len(l), chunk_length)]
    pool = Pool(nodes=cpus)
    f_dumps = cloudpickle.dumps(f)
    tuples = [(chunk, f_dumps, extra_data) for chunk in chunks]
    return pool.map(_process_whole_chunk, tuples)


def map_list_in_chunks(l, f, extra_data):
    '''
    A wrapper around ProcessPool.uimap that processes a list in chunks.
    Differs from `map_list_as_chunks` in that this method calls `f` once for each item in `l`.

    uimap already chunks but if you have extra data to pass in it will pickle
    it for every item. This function passes in the extra data to each chunk
    which significantly saves on pickling.
    https://stackoverflow.com/questions/53604048/iterating-the-results-of-a-multiprocessing-list-is-consuming-large-amounts-of-me

    Parameters
    ----------
    l : list
      the list
    f : function
      the function to process each item
      takes two parameters: item, extra_data
    extra_data : object
      the extra data to pass to each f
    '''
    cpus = cpu_count()
    chunk_length = max(1, int(len(l) / cpus))
    chunks = [l[x:x+chunk_length] for x in range(0, len(l), chunk_length)]
    pool = Pool(nodes=cpus)
    f_dumps = cloudpickle.dumps(f)
    tuples = [(chunk, f_dumps, extra_data) for chunk in chunks]
    mapped_chunks = pool.map(_process_chunk, tuples)
    return (item for chunk in mapped_chunks for item in chunk)


def _process_chunk(tup):
    '''Processes a chunk by invoking `f` for each item in the chunk.'''
    chunk, f_dumps, extra_data = tup
    f_loads = cloudpickle.loads(f_dumps)
    return [f_loads(i, extra_data) for i in chunk]


def _process_whole_chunk(tup):
      chunk, f_dumps, extra_data = tup
      f_loads = cloudpickle.loads(f_dumps)
      return f_loads(chunk, extra_data)
