/*
 * target_buffer_overflow.c
 * Fuzzinator - Vulnerable target: Stack buffer overflow
 *
 * Reads input from a file and copies it into a small stack buffer
 * using an unsafe function, triggering a crash on oversized input.
 *
 * Usage: ./target_buffer_overflow <input_file>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void vulnerable_function(const char *data, size_t len) {
    char buffer[32];

    /* Unsafe copy — no bounds check */
    if (len > 0) {
        memcpy(buffer, data, len);  /* overflow when len > 32 */
        buffer[len < 32 ? len : 31] = '\0';
    }

    /* Additional processing that touches the buffer */
    if (buffer[0] == 'F') {
        if (buffer[1] == 'U') {
            if (buffer[2] == 'Z') {
                if (buffer[3] == 'Z') {
                    /* Deep path — triggers more coverage edges */
                    volatile int x = buffer[4] * buffer[5];
                    (void)x;
                }
            }
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

    vulnerable_function(data, (size_t)fsize);

    free(data);
    return 0;
}
