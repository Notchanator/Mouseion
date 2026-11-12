# Border Analysis

How much of each US state's border is defined by water (ocean, lakes, or rivers)?

## Methodology

Uses Natural Earth 1:10m data (states, ocean, rivers, lakes), cached locally in `data/`. Lengths are measured in each state's own metric projection (`STATE_CRS` in `config.py`).

| Function | What it does |
|---|---|
| `loadData` | Loads the four layers, keeping only US states. |
| `clipLayerToState` | Clips ocean, rivers, and lakes to a padded box around the state. |
| `addRiverBuffer` | Widens river centerlines by `bufferSize` meters on each side, turning them into areas. |
| `unionWaterBoundaries` | Merges ocean, lakes, and buffered rivers into a single water shape. |
| `calculateWaterStateOverlap` | Intersects the state's border with the water shape and returns the water length, total length, and percentage. |
| `plot` | Maps the state with its water-defined border highlighted in red. |

Notes:

- Barrier islands and bays count toward the border. For example, both sides of Texas's Gulf islands are included.
- The river buffer width sets how close a border must run to a river to count as water.

## Results

River buffer: 1,000 m on each side.

| Rank | State | Water % | Water km | Total km |
|---:|---|---:|---:|---:|
| 1 | Hawaii | 100.0% | 1,455.4 | 1,455.4 |
| 2 | Alaska | 94.5% | 37,427.1 | 39,612.0 |
| 3 | New Jersey | 92.8% | 992.5 | 1,069.2 |
| 4 | Florida | 87.3% | 4,868.2 | 5,575.3 |
| 5 | Louisiana | 84.5% | 3,045.3 | 3,603.6 |
| 6 | Washington | 78.0% | 3,053.6 | 3,914.3 |
| 7 | Texas | 77.3% | 5,063.2 | 6,547.5 |
| 8 | Illinois | 75.6% | 1,523.9 | 2,014.8 |
| 9 | Michigan | 75.1% | 1,920.0 | 2,556.0 |
| 10 | Maryland | 73.1% | 2,037.6 | 2,788.2 |
| 11 | South Carolina | 71.7% | 1,261.4 | 1,758.1 |
| 12 | New York | 69.5% | 2,079.4 | 2,990.4 |
| 13 | Maine | 69.0% | 1,860.2 | 2,696.4 |
| 14 | California | 67.8% | 3,148.1 | 4,645.5 |
| 15 | Wisconsin | 66.9% | 1,340.3 | 2,004.2 |
| 16 | Massachusetts | 65.5% | 1,007.0 | 1,537.2 |
| 17 | Ohio | 65.0% | 1,011.0 | 1,556.0 |
| 18 | North Carolina | 64.0% | 2,627.2 | 4,106.6 |
| 19 | Rhode Island | 62.6% | 304.5 | 486.3 |
| 20 | Oregon | 62.6% | 1,550.8 | 2,477.3 |
| 21 | Georgia | 59.9% | 1,254.9 | 2,096.5 |
| 22 | Vermont | 57.9% | 458.0 | 791.5 |
| 23 | Kentucky | 57.4% | 1,137.0 | 1,979.8 |
| 24 | Minnesota | 55.9% | 1,462.2 | 2,615.8 |
| 25 | Mississippi | 54.4% | 1,037.2 | 1,905.8 |
| 26 | Indiana | 54.3% | 857.4 | 1,577.9 |
| 27 | Virginia | 53.6% | 1,782.0 | 3,327.2 |
| 28 | Delaware | 51.0% | 242.2 | 475.3 |
| 29 | Missouri | 48.2% | 1,064.9 | 2,211.1 |
| 30 | Iowa | 46.9% | 793.0 | 1,691.2 |
| 31 | New Hampshire | 42.1% | 333.2 | 790.7 |
| 32 | Connecticut | 37.7% | 216.3 | 573.3 |
| 33 | West Virginia | 33.9% | 573.2 | 1,691.8 |
| 34 | Alabama | 33.1% | 627.7 | 1,897.3 |
| 35 | Pennsylvania | 32.7% | 521.2 | 1,593.3 |
| 36 | Arkansas | 32.6% | 560.7 | 1,720.2 |
| 37 | Oklahoma | 30.8% | 733.5 | 2,382.0 |
| 38 | Nebraska | 27.4% | 572.7 | 2,088.3 |
| 39 | Arizona | 26.2% | 607.1 | 2,320.5 |
| 40 | North Dakota | 21.3% | 378.7 | 1,778.2 |
| 41 | Tennessee | 15.9% | 305.8 | 1,920.3 |
| 42 | South Dakota | 15.2% | 304.9 | 2,003.7 |
| 43 | Idaho | 14.7% | 390.8 | 2,665.6 |
| 44 | Nevada | 10.8% | 253.2 | 2,338.4 |
| 45 | Kansas | 9.7% | 191.8 | 1,975.9 |
| 46 | Utah | 2.7% | 53.1 | 1,970.9 |
| 47 | New Mexico | 2.2% | 51.9 | 2,389.2 |
| 48 | Wyoming | 2.2% | 43.9 | 2,030.4 |
| 49 | Colorado | 1.2% | 25.7 | 2,101.0 |
| 50 | Montana | 0.8% | 23.4 | 2,905.0 |
