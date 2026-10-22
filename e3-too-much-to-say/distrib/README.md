# Too Much to Say — participant files

Connect to the welcome kiosk and make its hidden `win` function run. The
included `overflow` binary is the **exact** ELF used by the challenge server.
You also get its C source as an introduction to stack buffer overflows.

## Run with Docker

```sh
docker compose up --build
nc 127.0.0.1 35007
```

## Run locally (Linux x86-64)

```sh
./overflow
```

Use a tool such as `nm` or `objdump` to find the address of `win`. The program
was compiled with no PIE and no stack canary. It is an x86-64 binary, so pack
addresses as **eight little-endian bytes**. The included `flag.txt` is only a
placeholder; the real flag is installed on the challenge server.

If you rebuild from `vuln.c` with `make`, the newly generated binary may have
slightly different function addresses from the hosted ELF.
