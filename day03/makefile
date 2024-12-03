AS   = tasm.exe
LINK = tlink.exe
RM   = del

all: day03_01.exe day03_02.exe

# Implicit rule for executables
.obj.exe:
        $(LINK) /v $*,,,\sources\mta\lib\mta

# Implicit rule for ASM source code
.asm.obj:
        $(AS) /zi $*

clean:
        $(RM) *.obj
