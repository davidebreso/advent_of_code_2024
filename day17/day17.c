#include <stdio.h>

int main(int argc, char **argv) {
    FILE *infile;

    if(argc != 2) {
        printf("Usage: %s nomefile\n", argv[0]);
        return 1;
    }
    
    infile = fopen(argv[1], "r");
    if(infile == NULL) {
        printf("Error while opening file %s, aborting.\n", argv[1]);
        return 2;
    }
    
    return 0;
}