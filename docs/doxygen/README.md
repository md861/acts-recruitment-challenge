# Doxygen Documentation

This directory contains the Doxygen configuration for generating source
documentation across the Python model, tests, scripts, frontend source, Go API
contracts, and project roadmap notes.

From the repository root:

```bash
doxygen docs/doxygen/Doxyfile
```

Generated HTML is written to:

```text
docs/doxygen/build/html/index.html
```

The generated `build/` directory is ignored so documentation can be rebuilt
locally without committing generated output.
