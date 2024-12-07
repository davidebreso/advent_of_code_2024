%TITLE "Advent of Code 2024 -- Day 6 -- Problem 2"

        IDEAL

        MODEL   small
        STACK   256

;------ Insert INCLUDE directives here

;------ Equates
bufLen          EQU     128
videoSeg        EQU     0A000h          ; EGA graphics memory is at A000h
videoSize       EQU     (320 * 200)/2   ; EGA 320x200 memory size

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

        mov     ax, 1                   ; Start with obstacle count = 1
@@10:
        mov     [count], ax             ; Save obstacle distance count
        push    ax                      ;  also on the stack
        call    Animate                 ; Animate guard movements
        cmp     [flag], 1               ; Test termination flag
        jz      @@20                    ;   stop search if = 1
        mov     si, offset videoBuf     ; DS:SI points to video buffer
        call    LoadScreen              ; Restore map with no path
        pop     ax                      ; Restore obstacle count
        inc     ax                      ; Increment for next search
        jmp     @@10                    ; Go to next try

;------ Print results to screen
@@20:
        mov     ah, 02h                 ; Video BIOS - Set cursor position
        mov     bh, 0                   ; Page is 0 in graphics mode
        mov     dx, 1800h               ; row 24, column 0
        int     10h                     ; Call BIOS to set pos
        mov     ax, [mapWidth]          ; Convert mapWidth
        mov     di, offset buffer       ;   to string in buffer
        mov     cx, 1                   ;   using at least one digit
        call    BinToAscDec             ; Do conversion
        mov     al, ' '                 ; Replace NULL with space
        stosb
        mov     ax, [mapHeight]         ; Convert mapHeight
        mov     cx, 1                   ;   using at least one digit
        call    BinToAscDec             ; Do conversion
        mov     al, ' '                 ; Replace NULL with space
        stosb
        mov     ax, [posX]              ; Convert [posX]
        mov     cx, 1                   ;   using at least one digit
        call    BinToAscDec             ; Do conversion
        mov     al, ' '                 ; Replace NULL with space
        stosb
        mov     ax, [posY]              ; Convert [posY]
        mov     cx, 1                   ;   using at least one digit
        call    BinToAscDec             ; Do conversion
        mov     al, ' '                 ; Replace NULL with space
        stosb
        mov     ax, [loops]             ; Convert [loops]
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

        mov     cx, 0                   ; CX is pixel X coordinate
        mov     dx, 1                   ; DX is pixel Y coordinate
        xor     bx, bx                  ; Page number is zero
        mov     ax, 0C07h               ; Video - Draw white pixel
        int     10h                     ; Call Video BIOS

;------ Read Input from STDIN one character at a time
@@10:
        push    cx                      ; Save current pixel position
        push    dx
        mov     ah, 3Fh                 ; DOS - Read from file
        xor     bx, bx                  ; STDIN file handle
        mov     cx, 1                   ; Read 1 char
        mov     dx, offset buffer       ; DS:DX points to input buffer
        int     21h                     ; Call DOS to read one line
        pop     dx                      ; Restore current pixel position
        pop     cx
        or      ax, ax                  ; Check if EOF
        jz      @@90                    ;   Terminate if EOF

        mov     ax, 0C0Bh               ; Video - write cyan pixel
        mov     bl, [buffer]            ; Load character in BL
        cmp     bl, 0Ah                 ; Is it LF?
        je      @@10                    ;  yes, skip to next char
        inc     cx                      ; Increment X coordinate
        cmp     bl, 0Dh                 ; Is it CR ?
        je      @@40                    ; Yes, go to line update
        cmp     bl, '^'                 ; Found start point?
        je      @@20                    ;   yes, jump
        cmp     bl, '#'                 ; Found obstacle?
        je      @@30                    ;   yes, go to pixel draw
        jmp     @@10                    ; Loop to next char
@@20:
        mov     al, 02h                 ; Set pixel color to green
        mov     [posX], cx              ; Save starting X position
        mov     [posY], dx              ; Save starting Y position
@@30:
        int     10h                     ; Call BIOS to write pixel
        jmp     @@10                    ; Loop to next char

@@40:
        mov     [mapWidth], cx          ; Save line width
        mov     ax, 0C07h               ; Video - write white pixel
        int     10h                     ; Call BIOS to draw border
        xor     cx, cx                  ; Reset X position to 0
        inc     dx                      ; Increment Y position
        int     10h                     ; Call Video BIOS
        jmp     @@10                    ; Loop

@@90:
        mov     [mapHeight], dx         ; Save Map height
        mov     cx, [mapWidth]          ; Prepare to draw [mapWidth] pixels
        mov     ax, 0C07h               ; Video - write white pixel
@@95:
        mov     dx, [mapHeight]         ; Load Y coordinate of lower border
        int     10h                     ; Call BIOS to draw lower border
        xor     dx, dx                  ; Set Y coordinate to 0
        int     10h                     ; Call BIOS to draw upper border
        loop    @@95                    ; Loop
        int     10h                     ; Draw pixel at (0, 0)

        ret                     ; Return to caller
ENDP    LoadMap
%NEWPAGE
;---------------------------------------------------------------------
; Animate       Compute guard movement and draw it to screen
;---------------------------------------------------------------------
; Input:
;       none
; Output:
;       [posX], [posY], [dir] updated
;       new obstacle is placed at [count] steps from start
;       [loops] incremented if loop found
; Registers:
;       ax, bx, cx, dx, di, si
;---------------------------------------------------------------------
PROC    Animate

        mov     cx, [posX]      ; Load X position in CX
        mov     dx, [posY]      ; Load Y position in CX
        mov     [dir], 00FFh    ; Initial direction of movement up (0, -1)
        mov     [flag], 1       ; Set termination flag to 1
@@10:
        mov     bx, [dir]       ; Restore direction of movement
        add     cl, bh          ; Compute next X position
        add     dl, bl          ; Compute next Y position
        xor     bx, bx          ; Set video page to 0
        mov     ah, 0Dh         ; Video BIOS - Read graphic pixel
        int     10h             ; Get pixel color in AL
        cmp     al, 07h         ; Is it white?
        je      @@90            ;   yes, terminate
        cmp     al, 0Bh         ; Is it cyan?
        je      @@70            ;   yes, turn right
        cmp     al, 00h         ; Is it black?
        jne     @@60            ;   no, go to check pixel color

;------ check obstacle limit
        dec     [count]         ; Decrement count
        jnz     @@60            ; Go to draw pixel if count != 0
        mov     [flag], 0       ; Obstacle placed, set termination flag to 0
        jmp     @@70            ; Go to turn right

;------ compute pixel color
@@60:
        mov     bx, [dir]       ; Direction of movement is in BH:BL
        shl     bh, 1           ; Multiply X movement by 2
        add     bl, bh          ;  and add it to Y movement
        add     bl, 03h         ; Add cyan to get pixel color
        cmp     al, bl          ; Is it the same of the current pixel?
        je      @@80            ;   yes, go to save result and terminate

        mov     ah, 0Ch         ; Video BIOS - write pixel
        mov     al, bl          ;   with pixel color in AL
        xor     bx, bx          ;   to page 0
        int     10h             ; Call BIOS to draw pixel
        jmp     @@10            ; Continue animation
@@70:
        mov     ax, 0C0Bh       ; Put obstacle cyan pixel in current position
        xor     bx, bx          ;   select page 0
        int     10h             ; Call BIOS to draw pixel
        mov     bx, [dir]       ; Restore current movement in BX
        sub     cl, bh          ; Revert movement
        sub     dl, bl
        neg     bl              ; 2-complement Y movement
        xchg    bl, bh          ; Swap X and Y movements
        mov     [dir], bx       ; Save new direction of movement
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
