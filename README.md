# Mouseion
The Mouseion is the Research Instituion of Alexandria that housed The Great Library of Alexandria, Plato's Academy, and Aristotle's Lyceum. This name was chosen for my personal repository because similar to the historical Mouseion this will repository will house my larger projects.

# Dependency Management

Each project is self-contained and declares its own dependencies in its subdirectory using that language's native manifest + lockfile. 

| Language | Manifest | Lockfile | Tool |
|----------|----------|----------|------|
| Python   | `pyproject.toml` | `uv.lock` | [uv](https://docs.astral.sh/uv/) |
| R        | `DESCRIPTION` | `renv.lock` | [renv](https://rstudio.github.io/renv/) *(planned)* |
| Java     | `pom.xml` | — | Maven *(planned, only if external deps are added)* |

# Git Structure

## Branch Creations
Try to keep each branch contained to be within each project (subfolder).
Each branch should be named with the following structure `{Project}-{Purpose}`; with the following shorthands per project:
- Mouseion : M
- GeniusStar : GS
- Wordle : W
- MemoryNinja: MN


