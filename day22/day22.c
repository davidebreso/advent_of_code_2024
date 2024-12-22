#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define BUFLEN 2048
#define STEPS 2000

int simulate(int secret, int steps) {
    // printf("%d\n", secret);
    for(int i = 0; i < steps; i++) {
        int newsecret;
        newsecret = secret << 6;                    // Multiply the secret by 64
        secret = (secret ^ newsecret) & 0xFFFFFF;   // Mix and prune
        newsecret = secret >> 5;                    // Divide the secret by 32
        secret = (secret ^ newsecret) & 0xFFFFFF;   // Mix and prune
        newsecret = secret << 11;                   // Multiply the secret by 2048
        secret = (secret ^ newsecret) & 0xFFFFFF;   // Mix and prune
        // printf("%d\n", secret); 
    }
    return secret;
}

/*
 * Compute the sequence of prices given initial secret and number of steps
 */
int *get_sequence(int secret, int steps) {
    int *sequence = malloc((steps + 1) * sizeof(int));
    
    sequence[0] = secret % 10;
    for(int i = 1; i <= steps; i++) {
        secret = simulate(secret, 1);
        sequence[i] = secret % 10;
    }
    
    return sequence;
}

void print_prices(int *prices, int* changes, int steps) {    
    for(int i = 0; i <= steps; i++) {
        printf("%d\t", prices[i]);
        int sequence = changes[i];
        for(int j = 0; j < 4; j++) {
            int8_t delta = (sequence & 0xFF000000) >> 24;
            sequence = sequence << 8;
            printf("%d, ", delta);
        }
        putchar('\n');
    }
}

/*
 * Compute a packed sequence of changes, given sequence of prices
 */
int *compute_changes(int *prices, int steps) {
    int *changes;
    int sequence, prev;
    
    if(steps < 4)  return NULL;

    changes = malloc((steps) * sizeof(int));   
    sequence = 0;
    prev = 0;
    for(int i = 0; i <= steps; i++) {
        int delta = prices[i] - prev;
        sequence = (sequence << 8) | (delta & 0xFF);
        changes[i] = sequence;
        prev = prices[i];
    }
    
    return changes;
}

/*
 * Compute number of bananas you can buy for each sequence
 */
int compute_bananas(int **prices, int **changes, int steps, int buyers) {
    int **bananas = malloc(buyers * sizeof(int *));
    int maxbananas = 0;
    
    for(int i = 0; i < buyers; i++) {
        bananas[i] = malloc((steps - 3) * sizeof(int));
        for(int j = 4; j <= steps; j++) {
            int sequence = changes[i][j];
            int currbananas = prices[i][j];
            /* Check if the current buyer has already seen the sequence */
            for(int k = 4; k < j;  k++) {
                if(changes[i][k] == sequence) {
                    currbananas = bananas[i][k];
                    goto save_result;
                }
            }
            /* Check previous buyers */
            for(int k = i - 1; k >= 0; k--) {
                for(int l = steps; l > 3; l--) {
                    if(changes[k][l] == sequence) {
                        currbananas += bananas[k][l];
                        goto save_result;
                    }
                }
            }
save_result:
            bananas[i][j] = currbananas;
            if(currbananas > maxbananas)
                maxbananas = currbananas;
        }
    }
    
    return maxbananas;
}

int main(int argc, char **argv) {
    FILE *infile;
    int buyers, secret = 123;
    int *prices[BUFLEN];
    int *changes[BUFLEN];
    int *bananas[BUFLEN];
    long key;

    if(argc != 2) {
        printf("Usage: %s nomefile\n", argv[0]);
        return 1;
    }
    
    infile = fopen(argv[1], "r");
    if(infile == NULL) {
        printf("Error while opening file %s, aborting.\n", argv[1]);
        return 2;
    }

    key = 0;
    buyers = 0;
    while(!feof(infile)) {
        int lastsecret;
        fscanf(infile, "%d\n", &secret);
        lastsecret = simulate(secret, STEPS);
        prices[buyers] = get_sequence(secret, STEPS);
        changes[buyers] = compute_changes(prices[buyers], STEPS);
        // printf("%d: %d\n", secret, lastsecret);
        // print_prices(prices[buyers], changes[buyers], STEPS);
        key += lastsecret;
        buyers++;
    }
    printf("Sum of all secrets is %ld\n", key);
    printf("Maximum number of bananas you can get is %d\n", 
            compute_bananas(prices, changes, STEPS, buyers));
        
    return 0;
}