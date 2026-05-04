#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void stack_overflow(char *input) {
    char buffer[32];
    // No bounds checking
    strcpy(buffer, input);  
    printf("Stack buffer: %s\n", buffer);
}

void heap_overflow(char *input) {
    char *buf = (char *)malloc(16);
    // Writing way beyond allocated memory
    strcpy(buf, input);
    printf("Heap buffer: %s\n", buf);
    free(buf);
}

void use_after_free(char *input) {
    char *buf = (char *)malloc(32);
    strcpy(buf, input);
    free(buf);

    // Use-after-free vulnerability
    printf("Use-after-free: %s\n", buf);
}

void double_free(char *input) {
    char *buf = (char *)malloc(32);
    strcpy(buf, input);
    free(buf);
    free(buf);  // Double free vulnerability
}

void format_string(char *input) {
    // Format string vulnerability
    printf(input);
    printf("\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <input>\n", argv[0]);
        return 1;
    }

    int choice = argv[1][0] % 5;  // random-ish path selection

    switch (choice) {
        case 0:
            stack_overflow(argv[1]);
            break;
        case 1:
            heap_overflow(argv[1]);
            break;
        case 2:
            use_after_free(argv[1]);
            break;
        case 3:
            double_free(argv[1]);
            break;
        case 4:
            format_string(argv[1]);
            break;
        default:
            break;
    }

    return 0;
}
