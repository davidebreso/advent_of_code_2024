AS   = tasm.exe
LINK = tlink.exe
RM   = del

OBJS = strings.obj strio.obj binasc.obj screen.obj keyboard.obj \
       diskerr.obj params.obj

all: day06_01.exe day06_02.exe

# Implicit rule for OBJ linking
.obj.exe:
        $(LINK) /v $*,,,\sources\mta\lib\mta

# Implicit rule for ASM source code
.asm.obj:
        $(AS) /zi $*

clean:
        $(RM) *.obj
        $(RM) *.bak
        $(RM) *.map
