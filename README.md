# PB benchmark

This repository is a deduplicated, reorganized clone of the benchmarks published at <https://www.cril.univ-artois.fr/PB26/>.

It collects every instance submitted to the Pseudo-Boolean competitions, in the normalized PB24 format. It does not include the selected subsets (`selected-*.tar`), which are incomplete and may repeat instances.

## Acknowledgements

The Pseudo-Boolean competitions and these benchmarks are maintained by Olivier Roussel (CRIL, Université d'Artois). This collection exists only because that archive is public. Thank you.

## Layout

Instances stay in the PB24 format, xz-compressed (a few files are uncompressed `.opb`), under `benchmarks/<category>/`. Two files are treated as the same instance when the SHA-256 of the body, ignoring comment lines, matches. The copy from the earlier competition is kept. 870 duplicates were removed. The 20 PB25 files under `parametric/php` sit outside a category directory in the source archive, but their bodies match existing DEC-LIN instances, so they were dropped as duplicates.

`benchmarks/manifest.tsv` records every kept and duplicate file. `benchmarks/duplicates.tsv` lists only the copies that were dropped. The instances themselves total 8.14 GiB (39,510 files). The largest file is 56.91 MiB.

`normalized-WBO.tar` stores `PARTIAL-LIN` and `SOFT-LIN` under a `WBO/` directory. Those two tracks are saved as their own categories.

| Category | Instances | Size | Contents |
|---|---:|---:|---|
| DEC-LIN | 20,232 | 1,396 MiB | Decision, linear constraints |
| DEC-NLC | 100 | 2 MiB | Decision, non-linear constraints |
| OPT-LIN | 17,485 | 6,837 MiB | Optimization, linear constraints |
| OPT-NLC | 674 | 21 MiB | Optimization, non-linear constraints |
| PARTIAL-LIN | 772 | 61 MiB | Partial soft constraints (WBO) |
| SOFT-LIN | 247 | 15 MiB | Soft constraints (WBO) |
| **Total** | **39,510** | **8.14 GiB** | |

## instance-list

`all/` is the full deduplicated set of submitted instances. Each `pbNN/` directory is the selected set for that competition, taken from `selected-PBNN.tar`. A selected file is recorded as the matching instance under `benchmarks/`. When the selection repeats an instance, the list keeps that file once. PB15 and the extra PB12 archive have no published selected set, so they have no directory here.

Each directory contains `{directory}-{category}-{class}.csv` files, for example `pb24/pb24-DEC-LIN-bigint.csv`. Columns are `path` and `intsize`. `path` is relative to `benchmarks/`. A file is written only when that combination has at least one instance.

`intsize` is the value in the first comment line: the number of bits needed to represent, for any constraint, the sum of the absolute values of the integers in that constraint (the objective is included). The competition expects solvers to use at least 64-bit integers, so `intsize <= 64` is `normalint` and `intsize > 64` is `bigint`. A signed 64-bit accumulator is safe only for `intsize <= 63`. Five instances have `intsize = 64` and are listed as `normalint`.

A few files in the older selected archives are not in the normalized collection (reduced MIP instances, and some PB09 SAT translations). Those are omitted: 291 from PB06, 431 from PB07, 169 from each of PB09, PB10, and PB11, 615 from PB16, and one each from PB12 and PB24. The PB25 and PB26 selections match completely.

| Directory | Instances | What it lists |
|---|---:|---|
| all | 39,510 | Every submitted instance |
| pb06 | 1,462 | Selected set |
| pb07 | 1,810 | Selected set |
| pb09 | 1,893 | Selected set |
| pb10 | 3,209 | Selected set |
| pb11 | 3,295 | Selected set |
| pb12 | 2,264 | Selected set |
| pb16 | 5,906 | Selected set |
| pb24 | 1,206 | Selected set |
| pb25 | 1,392 | Selected set |
| pb26 | 1,419 | Selected set |

Counts in `all/` by category and class:

| Category | normalint | bigint |
|---|---:|---:|
| DEC-LIN | 20,145 | 87 |
| DEC-NLC | 100 | 0 |
| OPT-LIN | 17,284 | 201 |
| OPT-NLC | 639 | 35 |
| PARTIAL-LIN | 772 | 0 |
| SOFT-LIN | 247 | 0 |
| **Total** | **39,187** | **323** |

## Data source

Page: <https://www.cril.univ-artois.fr/PB26/>

Normalized archives (every submitted instance, in the PB24 format):

| Archive | URL |
|---|---|
| normalized-PB06.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB06.tar |
| normalized-PB07.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB07.tar |
| normalized-PB09.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB09.tar |
| normalized-PB10.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB10.tar |
| normalized-PB11.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB11.tar |
| normalized-PB12.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB12.tar |
| normalized-extraPB12.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-extraPB12.tar |
| normalized-PB15eval.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB15eval.tar |
| normalized-PB16.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB16.tar |
| normalized-PB24.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-PB24.tar |
| normalized-PB25.tar | https://www.cril.univ-artois.fr/PB25/benchs/normalized-PB25.tar |
| normalized-WBO.tar | https://www.cril.univ-artois.fr/PB24/benchs/normalized-WBO.tar |
| normalized-PB26.tar | https://www.cril.univ-artois.fr/PB26/files/normalized-PB26.tar |

On the PB26 page, `files/normalized-PB6.tar` and `/PB26/benchs/normalized-PB26.tar` return 404. The file that exists is `/PB26/files/normalized-PB26.tar`, linked above.

Not included:

- `selected-*.tar`: the instances actually used in each competition. These archives repeat instances and do not contain the full set.
- `SampleByIntSize.tar`: one sample per category and `intsize`.
- Unnormalized PB26 submissions (qoblib market split, TSPLIB, CPMpy). Only the part folded into `normalized-PB26.tar` is included. The organizers dropped trivially unsatisfiable constraints, and when MIP or RCP filenames collided with older instances they kept the older encoding.

The original archives are in `src-archives/` (about 8.3 GiB). That directory is a local copy of the downloads, separate from `benchmarks/`.
