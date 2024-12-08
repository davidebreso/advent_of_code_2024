%TITLE "Advent of Code 2024 -- Day 6 -- Problem 2"

        IDEAL

        MODEL   small
        STACK   256

;------ Insert INCLUDE directives here

;------ Equates
bufLen          EQU     128
videoSeg        EQU     0A000h          ; EGA graphics memory is at A000h
videoSize       EQU     32 * 1024       ; Video and file read buffer size

        DATASEG

;------ If an error occurs and the program should halt, store an
;       appropriate error code in exCode and execute a JMP Exit
;       instruction. To do this from a submodule, declare the Exit
;       label in an EXTRN directive.

exCode          DB      0
oldMode         DB      0               ; Old video mode saved here
;------ DOS input buffer -----------------------------------------------
        ALIGN   2       ; Align to word bounday
buffer          DB      bufLen DUP(?)   ; Text buffer
;-----------------------------------------------------------------------
mapWidth        DW      0               ; Map width
mapHeight       DW      0               ; Map height
count           DW      1               ; Obstacle distance count
loops           DW      0               ; Number of loops
steps           DW      ?               ; Nuber of steps (local to Animate)
posX            DW      ?               ; Current guard position
posY            DW      ?               ;
dir             DW      ?               ; Current direction of movement
videoBuf        DB      videoSize DUP(?)        ; Video memory buffer
flag            DB      ?               ; Termination flag

        CODESEG

;------ From BINASC.OBJ

        EXTRN   BinToAscDec:Proc

;------ From STRIO.OBJ

        EXTRN   StrWrite:Proc, NewLine:Proc

Start:
        mov     ax, @data       ; Initalize DS to address
        mov     ds, ax          ;  of data segment
        mov     es, ax          ; Make ES=DS

;------ Save current video mode
        mov     ah, 0Fh                 ; Video BIOS - Get current video mode
        int     10h                     ; Call Video BIOS
        mov     [oldMode], al           ; Save current video mode

;------ Set EGA 320x200 16 color mode

        mov     ax, 000Dh               ; Video BIOS - Set video mode
        int     10h                     ; EGA 320x200 16 color graphics mode

;------ Load map and show animation

        call    LoadMap                 ; Read and draw map from STDIN
        mov     di, offset videoBuf     ; ES:DI points to video buffer
        call    SaveScreen              ; Save content of video memory

        mov     [count], 1              ; Start with obstacle count = 1
@@10:
        mov     ax, [count]             ; Set obstacle count
        call    Animate                 ; Animate guard movements
        cmp     [flag], 1               ; Test termination flag
        jz      @@20                    ;   stop search if = 1
        mov     si, offset videoBuf     ; DS:SI points to video buffer
        call    LoadScreen              ; Restore map with no path
        inc     [count]                 ; Increment obstacle count
        mov     ah, 1                   ; BIOS Keyboard - Check keystroke
        int     16h                     ; Call BIOS - ZF set if no keystroke
        jz      @@10                    ; Go to next try if no keystroke
        xor     ah, ah                  ; BIOS Keyboard - Get Keystroke
        int     16h                     ; Call BIOS to clear keystroke

;------ Print results to screen
@@20:
        mov     ah, 02h                 ; Video BIOS - Set cursor position
        mov     bh, 0                   ; Page is 0 in graphics mode
        mov     dx, 1800h               ; row 24, column 20
        int     10h                     ; Call BIOS to set pos
        mov     ax, [loops]             ; Convert loops
        mov     di, offset buffer       ;   to string in buffer
        mov     cx, 1                   ;   using at least one digit
        call    BinToAscDec             ; Do conversion
        mov     di, offset buffer       ; ES:DI points to full string
        call    StrWrite                ;  print result to screen

;------ Wait for keypress

        xor     ah, ah                  ; BIOS Keyboard - Get Keystroke
        int     16h                     ; Call BIOS to wait for keystroke

Exit:
;------ Restore video mode and active page
        mov     ah, 00h                 ; Video BIOS - Set video mode
        mov     al, [oldMode]           ; Restore video mode
        int     10h                     ; Call video BIOS
        mov     ah, 04Ch        ; DOS function: exit program
        mov     al, [exCode]    ; Return exit code value
        int     21h             ; Call DOS. Terminate program

%NEWPAGE
;---------------------------------------------------------------------
; LoadMap       Read map from STDIN and draw it to screen
;---------------------------------------------------------------------
; Input:
;       none
; Output:
;       [mapWidth], [mapHeigh], [posX], [posY] updated
; Registers:
;       ax, bx, cx, dx, di, si
;---------------------------------------------------------------------
PROC    LoadMap

        mov     bx, 0                   ; BX is pixel X coordinate
        mov     dx, 1                   ; DX is pixel Y coordinate
        mov     ah, 07h                 ; Draw white pixel
        call    DrawPixel               ; Call Video BIOS
        inc     bx                      ; Set initial position to (1,1)

;------ Read Input from STDIN, 32K at a time
@@10:
        push    bx                      ; Save current pixel position
        push    dx
        mov     ah, 3Fh                 ; DOS - Read from file
        xor     bx, bx                  ; STDIN file handle
        mov     cx, videoSize           ; Read videoSize char
        mov     dx, offset videoBuf     ;  into video buffer
        int     21h                     ; Call DOS to read input data
        pop     dx                      ; Restore current pixel position
        pop     bx                      ;   (X, Y) is in (BX, DX)
        or      ax, ax                  ; Check if EOF
        jz      @@80                    ;   Terminate if EOF
        xchg    ax, cx                  ; CX count character to parse
        mov     si, offset videoBuf     ; DS:SI points to next char
@@20:
        mov     ah, 07h                 ; Prepare to write border pixel
        lodsb                           ; Load character in AL, increment SI
        cmp     al, 0Ah                 ; Is it LF?
        je      @@30                    ;  yes, go to draw right border
        cmp     al, 0Dh                 ; Is it CR ?
        je      @@60                    ; Yes, go to line update
        cmp     al, '^'                 ; Found start point?
        je      @@50                    ;   yes, go to save start point
        cmp     al, '#'                 ; Found obstacle?
        jne     @@40                    ;   no, do not draw pixel
        mov     ah, 0Bh                 ; Set pixel color to cyan
@@30:
        call    DrawPixel               ; Call BIOS to write pixel
@@40:
        inc     bx                      ; Increment X coordinate
        loop    @@20                    ; Loop to next char, decrement CX
        jmp     @@10                    ; Go to load next block of input

@@50:
        mov     ah, 02h                 ; Set pixel color to green
        mov     [posX], bx              ; Save starting X position
        mov     [posY], dx              ; Save starting Y position
        jmp     @@30                    ; Go to draw pixel
@@60:
        mov     [mapWidth], bx          ; Save line width
        mov     ah, 07h                 ; Draw white pixel
        call    DrawPixel               ; Call BIOS to draw border
        xor     bx, bx                  ; Reset X position to 0
        inc     dx                      ; Increment Y position
        loop    @@20                    ; Loop to next char, decrement CX
        jmp     @@10                    ; Go to load next block of input

@@80:
        mov     [mapHeight], dx         ; Save Map height
        mov     bx, [mapWidth]          ; Prepare to draw [mapWidth] pixels
        mov     ah, 07h                 ; Prepare to write white pixel
@@90:
        mov     dx, [mapHeight]         ; Load Y coordinate of lower border
        call    DrawPixel               ; Call BIOS to draw lower border
        xor     dx, dx                  ; Set Y coordinate to 0
        call    DrawPixel               ; Call BIOS to draw upper border
        dec     bx                      ; Decrement X coordinate
        jnz     @@90                    ; Loop while X > 0
        call    DrawPixel               ; Draw pixel at (0, 0)

        ret                     ; Return to caller
ENDP    LoadMap
%NEWPAGE
;---------------------------------------------------------------------
; Animate       Compute guard movement and draw it to screen
;---------------------------------------------------------------------
; Input:
;       ax = obstacle count
; Output:
;       [posX], [posY], [dir] updated
;       new obstacle is placed at ax steps from start
;       [loops] incremented if loop found
; Registers:
;       ax, bx, cx, dx, di, si
;---------------------------------------------------------------------
PROC    Animate

        mov     bx, [posX]      ; Load X position in BX
        mov     dx, [posY]      ; Load Y position in DX
        mov     [dir], 00FFh    ; Initial direction of movement up (0, -1)
        mov     [flag], 1       ; Set termination flag to 1
        mov     [steps], ax     ; Save obstacle count to [steps]
@@10:
        mov     cx, [dir]       ; Restore direction of movement
        add     bl, ch          ; Compute next X position
        add     dl, cl          ; Compute next Y position
        call    ReadPixel       ; Get pixel color in AL
        cmp     al, 07h         ; Is it white?
        je      @@90            ;   yes, terminate
        cmp     al, 0Bh         ; Is it cyan?
        je      @@70            ;   yes, turn right
        cmp     al, 00h         ; Is it black?
        jne     @@60            ;   no, go to check pixel color

;------ check obstacle limit
        dec     [steps]         ; Decrement steps
        jnz     @@60            ; Go to draw pixel if count != 0
        mov     [flag], 0       ; Obstacle placed, set termination flag to 0
        jmp     @@70            ; Go to turn right

;------ compute pixel color
@@60:
        mov     cx, [dir]       ; Direction of movement is in CH:CL
        shl     ch, 1           ; Multiply X movement by 2
        add     cl, ch          ;  and add it to Y movement
        add     cl, 03h         ; Add cyan to get pixel color
        cmp     al, cl          ; Is it the same of the current pixel?
        je      @@80            ;   yes, go to save result and terminate

        mov     ah, cl          ; Set pixel color in AH
        call    DrawPixel       ; Call BIOS to draw pixel
        jmp     @@10            ; Continue animation
@@70:
        mov     ah, 0Bh         ; Put obstacle cyan pixel in current position
        call    DrawPixel       ; Call BIOS to draw pixel
        mov     cx, [dir]       ; Restore current movement in BX
        sub     bl, ch          ; Revert movement
        sub     dl, cl
        neg     cl              ; 2-complement Y movement
        xchg    cl, ch          ; Swap X and Y movements
        mov     [dir], cx       ; Save new direction of movement
        jmp     @@10            ; Repeat movement

;------ Found a loop. Save result and print obstacle coordinates
@@80:
        inc     [loops]         ; Increment loop counter
        mov     [flag], 0       ; Set termination flag to 0
@@90:
        ret                     ; Return to caller
ENDP    Animate
%NEWPAGE
;---------------------------------------------------------------------
; DrawPixel     Use BIOS calls to draw pixel to screen
;---------------------------------------------------------------------
; Input:
;       ah = pixel color
;       bx = X coordinate
;       dx = Y coordinate
; Output:
;       none
; Registers:
;       none
;---------------------------------------------------------------------
PROC    DrawPixel
        push    ax                      ; Save registers
        push    bx
        push    cx
        push    dx
        xchg    al, ah                  ; Put pixel color in AL
        mov     ah, 0Ch                 ; Video - write pixel
        xchg    cx, bx                  ;   X coordinate in CX
        xor     bx, bx                  ;   select page 0
        int     10h                     ; Call BIOS to draw pixel
        pop     dx                      ; Restore registers
        pop     cx
        pop     bx
        pop     ax
        ret                             ; Return to caller
ENDP    DrawPixel
%NEWPAGE
;---------------------------------------------------------------------
; ReadPixel     Use BIOS calls to read pixel color from screen
;---------------------------------------------------------------------
; Input:
;       bx = X coordinate
;       dx = Y coordinate
; Output:
;       al = color of pixel at (X, Y)
; Registers:
;       ax
;---------------------------------------------------------------------
PROC    ReadPixel
        push    bx                      ; Save registers
        push    cx
        push    dx
        mov     ah, 0Dh                 ; Video - read pixel
        xchg    cx, bx                  ;   with X coordinate in cx
        xor     bx, bx                  ;   from page 0
        int     10h                     ; Call BIOS to read pixel
        pop     dx                      ; Restore registers
        pop     cx
        pop     bx
        ret                             ; Return to caller
ENDP    ReadPixel
%NEWPAGE
;---------------------------------------------------------------------
; SaveScreen            ; Save video memory to buffer
;---------------------------------------------------------------------
; Input:
;       ES:DI = address of buffer
; Output:
;       content of video window saved to buffer
; Registers:
;       ax, bx, cx, dx, di, si
;---------------------------------------------------------------------
PROC    SaveScreen
        push    ds                      ; Save segment registers
        push    es
        mov     bx, [mapWidth]          ; BX is map width
        add     bx, 16                  ; Round up to 16-bit multiple
        mov     cl, 4                   ; Divide BX by 16 by shifting
        shr     bx, cl                  ; BX is words per line to copy
        mov     cx, [mapHeight]         ; CX is index of last line to copy
        inc     cx                      ;  plus one is no. of lines to copy
        mov     ax, videoSeg            ; CX points to Video segment
        mov     ds, ax                  ; DS points to Video segment
        mov     dx, 03CEh               ; Select EGA graphics registers
        mov     ax, 0005h               ; Select Read Mode 0
        out     dx, ax                  ;  write to EGA register
        mov     ax, 0304h               ; Start copy from plane 3

@@10:
        push    ax                      ; Save plane number to stack
        push    cx                      ; Save lines to copy to stack
        out     dx, ax                  ; Select current plane
        xor     si, si                  ; Start copy at videoSeg:0

;------ Copy one plane of data
@@20:
        xchg    ax, cx                  ; Save lines to copy to AX
        push    si                      ; Save start of line to stack
        mov     cx, bx                  ; Copy one line of planar memory
        rep     movsw
        pop     si                      ; Restore SI to start of line
        add     si, 40                  ; DS:SI points to next line
        xchg    cx, ax                  ; Restore CX to lines to copy
        loop    @@20                    ; Loop to copy another line

        pop     cx                      ; CX is number of lines to copy
        pop     ax                      ; AX is number of planes
        sub     ah, 1                   ; Decrement plane number
        jnc     @@10                    ; Loop if there are planes to copy

        pop     es                      ; Restore segment registers
        pop     ds
        ret                             ; Return to caller
ENDP    SaveScreen
%NEWPAGE
;---------------------------------------------------------------------
; LoadScreen            ; Load video memory from buffer
;---------------------------------------------------------------------
; Input:
;       DS:SI = address of buffer
; Output:
;       content of buffer copied to video memory
; Registers:
;       ax, bx, cx, dx, di, si
;---------------------------------------------------------------------
PROC    LoadScreen
        push    ds                      ; Save segment registers
        push    es
        mov     bx, [mapWidth]          ; BX is map width
        add     bx, 15                  ; Round up to 16-bit multiple
        mov     cl, 4                   ; Divide BX by 16 by shifting
        shr     bx, cl                  ; BX is words per line to copy
        mov     cx, [mapHeight]         ; CX is index of last line to copy
        inc     cx                      ;  plus one is no. of lines to copy
        mov     ax, videoSeg            ; AX points to Video segment
        mov     es, ax                  ; ES points to Video segment
        mov     dx, 03CEh               ; Select EGA graphics registers
        mov     ax, 0005h               ; Select Write Mode 0
        out     dx, ax                  ;  write to EGA register
        mov     ax, 0003h               ; Set Rotate Register to 0
        out     dx, ax                  ;  write to EGA register
        mov     ax, 0FF08h              ; Set Bit Mask Register to 0FFh
        out     dx, ax                  ;  write to EGA register
        mov     ax, 0802h               ; Start copy from plane 4
        mov     dx, 03C4h               ; Select EGA register

@@10:
        push    ax                      ; Save plane number to stack
        push    cx                      ; Save lines to copy to stack
        out     dx, ax                  ; Select current plane
        xor     di, di                  ; Start copy at videoSeg:0

;------ Copy one plane of data
@@20:
        xchg    ax, cx                  ; Save lines to copy to AX
        push    di                      ; Save start of line to stack
        mov     cx, bx                  ; Copy one line of planar memory
        rep     movsw
        pop     di                      ; Restore DI to start of line
        add     di, 40                  ; ES:DI points to next line
        xchg    cx, ax                  ; Restore CX to lines to copy
        loop    @@20                    ; Loop to copy another line

        pop     cx                      ; CX is number of lines to copy
        pop     ax                      ; BX is number of planes
        shr     ah, 1                   ; Decrement plane number
        jnz     @@10                    ; Loop if there are planes to copy

        mov     ax, 0F02h               ; Restore normal plane mask
        mov     dx, 03C4h               ;   select EGA register
        out     dx, ax                  ;   write to EGA register
        pop     es                      ; Restore segment registers
        pop     ds
        ret                             ; Return to caller
ENDP    LoadScreen

        END     Start           ; End of program / entry point
