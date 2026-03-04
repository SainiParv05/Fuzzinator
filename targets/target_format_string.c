/*
 * target_format_string.c
 * Fuzzinator - Vulnerable target: Format string vulnerability
 *
 * Reads input from a file and passes it directly to printf(),
 * allowing format string exploitation (e.g., %s, %x, %n).
 *
 * Usage: ./target_format_string <input_file>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_input(const char *data, size_t len) {
    char buffer[256];

    if (len >= sizeof(buffer))
        len = sizeof(buffer) - 1;

    memcpy(buffer, data, len);
    buffer[len] = '\0';

    /* VULNERABLE: user-controlled format string */
    printf(buffer);
    printf("\n");

    /* Some branches to create interesting coverage */
    if (len > 2 && buffer[0] == '%') {
        if (buffer[1] == 'n') {
            /* format string write — very dangerous */
            volatile int sink = 0;
            (void)sink;
        } else if (buffer[1] == 'x') {
            volatile int leak = 42;
            (void)leak;
        } else if (buffer[1] == 's') {
            volatile int read_mem = 99;
            (void)read_mem;
        }
    }

    if (len > 5) {
        if (memcmp(buffer, "CRASH", 5) == 0) {
            /* Intentional null dereference */
            char *p = NULL;
            *p = 'X';
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "rb");
    if (!fp) {
        perror("fopen");
        return 1;
    }

    fseek(fp, 0, SEEK_END);
    long fsize = ftell(fp);
    rewind(fp);

    if (fsize <= 0 || fsize > 4096) {
        fclose(fp);
        return 1;
    }

    char *data = (char *)malloc(fsize);
    if (!data) {
        fclose(fp);
        return 1;
    }

    fread(data, 1, fsize, fp);
    fclose(fp);

    process_input(data, (size_t)fsize);

    free(data);
    return 0;
}
