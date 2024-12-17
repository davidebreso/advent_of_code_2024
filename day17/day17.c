#include <stdio.h>
#include <string.h>

#define BUFLEN 1024

struct registers {
  int a;
  int b;
  int c;
  int pc; 
  char *output; 
};

int jumps = 0;

int combo(int operand, const struct registers *regs) {
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

void adv(int operand, struct registers *regs) {
    regs->a = regs->a >> combo(operand, regs);
    regs->pc += 2;
}

void bxl(int operand, struct registers *regs) {
    regs->b = regs->b ^ operand;
    regs->pc += 2;
}

void bst(int operand, struct registers *regs) {
    regs->b = combo(operand, regs) & 7;
    regs->pc += 2;
}

void jnz(int operand, struct registers *regs) {
    if(regs->a == 0) {
        regs->pc += 2;
    } else {
        regs->pc = operand;
        jumps++;    
    }
}

void bxc(int operand, struct registers *regs) {
    regs->b = regs->b ^ regs->c;
    regs->pc += 2;
}

void out(int operand, struct registers *regs) {
    regs->output += sprintf(regs->output, "%d,", combo(operand, regs) & 7);
    regs->pc += 2;
}

void bdv(int operand, struct registers *regs) {
    regs->b = regs->a >> combo(operand, regs);
    regs->pc += 2;
}

void cdv(int operand, struct registers *regs) {
    regs->c = regs->a >> combo(operand, regs);
    regs->pc += 2;
}

void print_registers(const struct registers *regs) {
    printf("A: %d\tB: %d\tC: %d\tPC: %d\n", regs->a, regs->b, regs->c, regs->pc);
}

// opcodes is an array of function pointers
void (*opcodes[])(int operand, struct registers *regs) = {
    adv, bxl, bst, jnz, bxc, out, bdv, cdv
};

int main(int argc, char **argv) {
    FILE *infile;
    struct registers regs;
    char program[BUFLEN], output[BUFLEN];
    int progsize;

    if(argc != 2) {
        printf("Usage: %s nomefile\n", argv[0]);
        return 1;
    }
    
    infile = fopen(argv[1], "r");
    if(infile == NULL) {
        printf("Error while opening file %s, aborting.\n", argv[1]);
        return 2;
    }
    
    fscanf(infile, "Register A: %d\n", &regs.a);
    fscanf(infile, "Register B: %d\n", &regs.b);
    fscanf(infile, "Register C: %d\n", &regs.c);
    regs.pc = 0;
    regs.output = output;
        
    fscanf(infile, "Program: %s", program);
    progsize = strlen(program);
    if(program[progsize - 1] == '\n') {
        printf("Newline at end of program!\n");
    }

    print_registers(&regs);    
    printf("Program: %s\n", program);

    for(int i = 0;  ; i++) {
        struct registers copy;
        jumps = 0;
        if(i < 0) break;
        copy.a = i;
        copy.b = regs.b;
        copy.c = regs.c;
        copy.pc = 0;
        copy.output = output;
        while(2 * copy.pc < progsize && jumps < progsize) {
            int opcode = program[2 * copy.pc] - '0';
            int operand = program[2 * (copy.pc + 1)] - '0';
            //printf("Instruction %d,%d\n", opcode, operand);
            opcodes[opcode](operand, &copy);
            //print_registers(&regs);
            //getchar();
        }
        *(copy.output - 1) = '\0';
        if(strcmp(program, output) == 0) {
            printf("\nFor A=%d, program outputs a copy of itself!\n", i);
            break;
        } 
/*        if (i % 65536 == 0) {
            fflush(stdout);
            putchar('.');
        } */
        // getchar();
    }
    puts(output);    
    return 0;
}