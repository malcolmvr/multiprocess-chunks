# multiprocess_chunks

Chunk-based, multiprocess processing of iterables.
Uses the `multiprocess` package to perform the multiprocessization.
Uses the `cloudpickle` to pickle hard-to-pickle objects.

#### Why is this useful?

When using the built-in Python `multiprocessing.Pool.map` method the items being iterated are individually pickled. This can lead to a lot of pickling which can negatively affect performance. This is particularly true, and not necessarily obvious, if extra data is passed into the `f` function via a lambda. For example:

```
from multiprocessing import Pool
d = {...} # a large dict of some sort
p.map(lamda x: x + d[x], [1, 2, 3, ...])
```

In this case both `x` and `d` are pickled, individually, for every item in `[1, 2, 3, ...]`.

The methods in this package divide the `[1, 2, 3, ...]` list into chunks and pickle each chunk and `d` a small number of times.

## Installation

```
pip install multiprocess-chunks
```

## Usage

There are two methods to choose from: `map_list_as_chunks` and `map_list_in_chunks`.

#### map_list_as_chunks

This method divides the iterable that is passed to it into chunks.
The chunks are then processed in multiprocess.
It returns the mapped chunks.

Parameters:
`def map_list_as_chunks(l, f, extra_data, cpus=None, max_chunk_size=None`)

- `l`: The iterable to process in multiprocess.
- `f`: The function that processes each chunk. It takes two parameters: - `chunk, extra_data`
- `extra_data`: Data that is passed into `f` for each chunk.
- `cpus`: The number of CPUs to use. If `None` the number of cores on the system will be used. This value decides how many chunks to create.
- `max_chunk_size`: Limits the chunk size.

Example:

```
from multiprocess_chunks import map_list_as_chunks

l = range(0, 10)
f = lambda chunk, ed: [c * ed for c in chunk]
result = map_list_as_chunks(l, f, 5, 2)
# result = [ [0, 5, 10, 15, 20], [25, 30, 35, 40, 45] ]
```

#### map_list_in_chunks

This method divides the iterable that is passed to it into chunks.
The chunks are then processed in multiprocess.
It unwinds the processed chunks to return the processed items.

Parameters:
`def map_list_in_chunks(l, f, extra_data)`

- `l`: The iterable to process in multiprocess.
- `f`: The function that processes each chunk. It takes two parameters: `item, extra_data`
- `extra_data`: Data that is passed into `f` for each chunk.

Example:

```
from multiprocess_chunks import map_list_in_chunks

l = range(0, 10)
f = lambda item, ed: item * ed
result = map_list_in_chunks(l, f, 5)
# result = [0, 5, 10, 15, 20 25, 30, 35, 40, 45]
```

Essentially, `map_list_in_chunks` gives the same output as `multiprocessing.Pool.map` but, behind the scenes, it is chunking and being efficient about pickling.

#### A note on pickling

This package uses the `pathos` package to perform the multiprocessization and the `cloudpickle` package to perform pickling. This allows it to pickle objects that Python's built-in `multiprocessing` cannot.

#### Performance

How much better will your code perform? There are many factors at play here. The only way to know is to do your own timings.
