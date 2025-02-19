This file only describes the most important changes. A more detailed history
can be found in the version control log.

# 0.0.6

- `bf_to_function` and experimental JIT on x86_64 Linux.
- `bf_to_shared` and `bf_file_to_shared` no longer require the user to provide
a path to asm file.

# 0.0.5

- i386 support.

# 0.0.4

- 32-bit ARM (as well as Thumb-2) support.

# 0.0.3

- RISCV64 support.
- Conformance to standard bf: EOF is treated as 0.

# 0.0.2

- 64-bit ARM support.
- On AMD64, Intel syntax is supported and becomes the default.
- Optimizations for `++`, `<<<` and similar sequences.
- Dead code elimination for consecutve loops.

# 0.0.1 (Initial Version)

- Compile bf (one-byte-cell variant) to AT&T syntax AMD64 assembly,
which can be assembled to a shared library.
