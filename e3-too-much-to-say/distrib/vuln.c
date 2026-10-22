#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* A reachable function is deliberately omitted from the normal call path. */
__attribute__((noinline, used)) void win(void) {
    const char *path = getenv("FLAG_PATH");
    if (path == NULL) {
        path = "flag.txt";
    }

    int fd = open(path, O_RDONLY);
    if (fd < 0) {
        const char error[] = "Could not open flag.txt.\n";
        write(STDOUT_FILENO, error, sizeof(error) - 1);
        _exit(1);
    }

    char flag[128];
    ssize_t n = read(fd, flag, sizeof(flag));
    close(fd);
    const char banner[] = "You found the hidden function!\n";
    write(STDOUT_FILENO, banner, sizeof(banner) - 1);
    if (n > 0) {
        write(STDOUT_FILENO, flag, (size_t)n);
    }
    _exit(0);
}

__attribute__((noinline)) void welcome(void) {
    char name[32];
    puts("Welcome to the NUT helpdesk kiosk!");
    puts("What is your name?");
    /* Intentional vulnerability: reads far beyond the 32-byte buffer. */
    read(STDIN_FILENO, name, 160);
    puts("Thank you. Your request has been recorded.");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    welcome();
    puts("Session closed.");
    return 0;
}
