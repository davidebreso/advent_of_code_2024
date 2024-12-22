#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <uthash.h>

#define BUFLEN 2048
#define STEPS 2000

struct strategy {
    int sequence;               /* Packed price change sequence (Key) */
    int lastbuyer;              /* Last buyer that has seen the sequence */
    int bananas;                /* Current return of the strategy */
    
    UT_hash_handle hh;          /* makes this structure hashable */
};

struct strategy *market = NULL;

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
 * Compute maximum number of bananas you can buy
 */
int compute_bananas(int **prices, int **changes, int steps, int buyers) {
    struct strategy *s;
    int maxbananas = 0;
    
    for(int i = 0; i < buyers; i++) {
        for(int j = 4; j <= steps; j++) {
            int sequence = changes[i][j];
            int currbananas = prices[i][j];
            /* Check if the sequence has been previously seen */
            HASH_FIND_INT(market, &sequence, s);
            if(s == NULL) {
                /* First time for this sequence, add strategy to market */
                s = (struct strategy *)malloc(sizeof(struct strategy));
                s->sequence = sequence;
                s->lastbuyer = i;
                s->bananas = currbananas;
                HASH_ADD_INT(market, sequence, s);  /* sequence: name of key field */
            } else if(s->lastbuyer < i) {
                /* First time for this buyer, update strategy */
                s->lastbuyer = i;
                s->bananas += currbananas;
            }
            if(s->bananas > maxbananas) {
                maxbananas = s->bananas;
            }
        }
    }
    
    return maxbananas;
}

int main(int argc, char **argv) {
    FILE *infile;
    int buyers, secret = 123;
    int *prices[BUFLEN];
    int *changes[BUFLEN];
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
        key += lastsecret;
        buyers++;
    }
    printf("Sum of all secrets is %ld\n", key);
    printf("Maximum number of bananas you can get is %d\n", 
            compute_bananas(prices, changes, STEPS, buyers));
        
    return 0;
}