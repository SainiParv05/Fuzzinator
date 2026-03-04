/*
 * target_maze.c
 * Fuzzinator - Vulnerable target: Maze challenge
 *
 * Requires a specific sequence of bytes to navigate through a maze
 * of conditional branches. Reaching the end triggers a crash.
 * This exercises coverage-guided exploration.
 *
 * Usage: ./target_maze <input_file>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void maze(const unsigned char *data, size_t len) {
    /* The maze requires at least 8 bytes to reach the crash */
    if (len < 8) return;

    /* Room 1 */
    if (data[0] == 'M') {
        /* Room 2 */
        if (data[1] == 'A') {
            /* Room 3 */
            if (data[2] == 'Z') {
                /* Room 4 */
                if (data[3] == 'E') {
                    /* Room 5 — numeric check */
                    if (data[4] == 0x42) {
                        /* Room 6 — XOR check */
                        if ((data[5] ^ 0xAA) == 0x55) {
                            /* Room 7 — sum check */
                            if ((data[6] + data[7]) == 0xCC) {
                                /* MAZE SOLVED — trigger crash */
                                printf("MAZE SOLVED!\n");
                                char *p = NULL;
                                *p = 'W';  /* null deref crash */
                            }

                            /* Partial room 7 — close but wrong sum */
                            volatile int almost = data[6] * data[7];
                            (void)almost;
                        }

                        /* Partial room 6 */
                        volatile int partial6 = data[5];
                        (void)partial6;
                    }

                    /* Partial room 5 */
                    volatile int partial5 = data[4];
                    (void)partial5;
                }

                /* Dead-end branch */
                if (data[3] == 'X') {
                    volatile int dead1 = 1;
                    (void)dead1;
                }
            }

            /* Another dead-end */
            if (data[2] == 'Q') {
                volatile int dead2 = 2;
                (void)dead2;
            }
        }

        /* Wrong turn at room 2 */
        if (data[1] == 'B') {
            volatile int wrong = 3;
            (void)wrong;
        }
    }

    /* Alternative entry — different maze path */
    if (data[0] == 'X') {
        if (len >= 4 && memcmp(data, "XYZW", 4) == 0) {
            /* Alternative crash path */
            int *p = NULL;
            *p = 42;
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

    unsigned char *data = (unsigned char *)malloc(fsize);
    if (!data) {
        fclose(fp);
        return 1;
    }

    fread(data, 1, fsize, fp);
    fclose(fp);

    maze(data, (size_t)fsize);

    free(data);
    return 0;
}
