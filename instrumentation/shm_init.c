/*
 * shm_init.c
 * Fuzzinator — Shared memory coverage instrumentation
 *
 * Implements the __sanitizer_cov_trace_pc callback used by
 * clang's -fsanitize-coverage=trace-pc. Each time a basic block
 * is executed, this callback hashes the return address and marks
 * the corresponding byte in a shared memory bitmap.
 *
 * Bitmap location: /dev/shm/fuzz_bitmap
 * Bitmap size: 65536 bytes (64 KB)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdint.h>

#define SHM_NAME   "/fuzz_bitmap"
#define BITMAP_SIZE 65536

static uint8_t *bitmap = NULL;
static uint64_t prev_pc = 0;

/* Initialize shared memory bitmap */
__attribute__((constructor))
static void __fuzz_init(void) {
    int fd = shm_open(SHM_NAME, O_RDWR, 0666);
    if (fd < 0) {
        /* Create if it doesn't exist */
        fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
        if (fd < 0) {
            perror("shm_open");
            return;
        }
        if (ftruncate(fd, BITMAP_SIZE) < 0) {
            perror("ftruncate");
            close(fd);
            return;
        }
    }

    bitmap = (uint8_t *)mmap(NULL, BITMAP_SIZE, PROT_READ | PROT_WRITE,
                             MAP_SHARED, fd, 0);
    close(fd);

    if (bitmap == MAP_FAILED) {
        bitmap = NULL;
        perror("mmap");
    }
}

/*
 * Clang sanitizer coverage callback.
 * Called at every basic block entry when compiled with
 * -fsanitize-coverage=trace-pc.
 *
 * We use a simple edge hashing scheme:
 *   edge_id = (prev_pc >> 1) XOR current_pc
 * This captures transitions between basic blocks (edges).
 */
void __sanitizer_cov_trace_pc(void) {
    if (!bitmap) return;

    uint64_t current_pc = (uint64_t)__builtin_return_address(0);
    uint64_t edge_id = (prev_pc >> 1) ^ current_pc;

    bitmap[edge_id % BITMAP_SIZE]++;
    prev_pc = current_pc;
}
