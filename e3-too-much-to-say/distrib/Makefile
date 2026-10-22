CC ?= gcc
CFLAGS = -O0 -g -fno-stack-protector -fno-pie -fno-omit-frame-pointer -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0 -Wno-stringop-overflow
LDFLAGS = -no-pie -Wl,-z,noexecstack -Wl,-z,relro,-z,now

all: overflow

overflow: vuln.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

clean:
	rm -f overflow
