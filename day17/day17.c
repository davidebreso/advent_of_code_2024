#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFLEN 128

struct registers {
  long a;
  long b;
  long c;
  long pc; 
  char *output; 
};

long jumps = 0;

long combo(long operand, const struct registers *regs) {
    if (operand < 4) return operand;
    switch(operand) {
        case 4:
            return regs->a;
        case 5:
            return regs->b;
        case 6:
            return regs->c;
    }
    printf("\nInvalid combo operand!\n");
    return -1;
}

void adv(long operand, struct registers *regs) {
    regs->a = regs->a >> combo(operand, regs);
    regs->pc += 2;
}

void bxl(long operand, struct registers *regs) {
    regs->b = regs->b ^ operand;
    regs->pc += 2;
}

void bst(long operand, struct registers *regs) {
    regs->b = combo(operand, regs) & 7;
    regs->pc += 2;
}

void jnz(long operand, struct registers *regs) {
    if(regs->a == 0) {
        regs->pc += 2;
    } else {
        regs->pc = operand;
        jumps++;    
    }
}

void bxc(long operand, struct registers *regs) {
    regs->b = regs->b ^ regs->c;
    regs->pc += 2;
}

void out(long operand, struct registers *regs) {
    regs->output += sprintf(regs->output, "%ld,", combo(operand, regs) & 7);
    regs->pc += 2;
}

void bdv(long operand, struct registers *regs) {
    regs->b = regs->a >> combo(operand, regs);
    regs->pc += 2;
}

void cdv(long operand, struct registers *regs) {
    regs->c = regs->a >> combo(operand, regs);
    regs->pc += 2;
}

void print_registers(const struct registers *regs) {
    printf("A: %ld\tB: %ld\tC: %ld\tPC: %ld\n", regs->a, regs->b, regs->c, regs->pc);
}

// opcodes is an array of function pointers
void (*opcodes[])(long operand, struct registers *regs) = {
    adv, bxl, bst, jnz, bxc, out, bdv, cdv
};

char *execute(const char *program, struct registers *regs) {
    char *output = malloc(BUFLEN);
    long progsize = strlen(program);
    
    regs->pc = 0;
    regs->output = output;    
    while(2 * regs->pc < progsize) {
        long opcode = program[2 * regs->pc] - '0';
        long operand = program[2 * (regs->pc + 1)] - '0';
        opcodes[opcode](operand, regs);
    }
    *(regs->output - 1) = '\0';
    return output;
}

long check_subkey(long key, int j, char *program, struct registers *regs) {
    int progsize = strlen(program);
    char *output;
    
    if (j > progsize / 2) return key;
    
    // printf("Checking for %c\n", program[progsize - 2*j - 1]);
    for(long i = 0; i < 8; i++) {
        struct registers copy;
        char digit;
        long subkey = i << 3 * ((progsize / 2) - j);
        copy.a = key + subkey;
        copy.b = regs->b;
        copy.c = regs->c;
        output = execute(program, &copy);
        digit = *(copy.output - 2*j - 2);
        if(digit == program[progsize - 2*j - 1]){
            // printf("%lo: %s\n", key + subkey, output);
            subkey = check_subkey(key + subkey, j + 1, program, regs);
            if(subkey >= 0) {
                return subkey;
            }
        }
    }
    return -1;
}


int main(int argc, char **argv) {
    FILE *infile;
    struct registers regs, copy;
    char program[BUFLEN];
    char *output;
    int progsize;
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
    
    fscanf(infile, "Register A: %ld\n", &regs.a);
    fscanf(infile, "Register B: %ld\n", &regs.b);
    fscanf(infile, "Register C: %ld\n", &regs.c);
    regs.pc = 0;
    regs.output = output;
        
    fscanf(infile, "Program: %s", program);
    progsize = strlen(program);
    if(program[progsize - 1] == '\n') {
        printf("Newline at end of program!\n");
    }

    print_registers(&regs);    
    printf("Program: %s\n", program);
    
    copy = regs;
    output = execute(program, &copy);
    printf("Program output: %s\n", output);
    
    for(long i = 1; i < 8; i++) {
        copy = regs;
        char digit;
        key = i << 3 * (progsize / 2);
        copy.a = key;
        output = execute(program, &copy);
        digit = *(copy.output - 2);
        if(digit == program[progsize - 1]){
            key = check_subkey(key, 1, program, &regs);
            if(key >= 0) break;
        }
    }
    printf("Found QUINE for A = %ld\n", key);
    
    return 0;
}