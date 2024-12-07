%TITLE "Advent of Code 2024 -- Day 6 -- Problem 1"

        IDEAL

        MODEL   small
        STACK   256

;------ Insert INCLUDE directives here

;------ Equates
bufLen          EQU     128

        DATASEG

;------ If an error occurs and the program should halt, store an
;       appropriate error code in exCode and execute a JMP Exit
;       instruction. To do this from a submodule, declare the Exit
;       label in an EXTRN directive.

exCode          DB      0
;------ DOS input buffer -----------------------------------------------
buffer          DB      bufLen DUP(?)   ; Text buffer
;-----------------------------------------------------------------------
mapWidth        DW      0               ; Map width
mapHeight       DW      0               ; Map height
count           DW      0               ; Pink Pixel count
posX            DW      ?               ; Current guard position
posY            DW      ?               ;
oldMode         DB      ?               ; Old video mode saved here


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

;------ Set CGA 320x200 4 color mode

        mov     ah, 00h                 ; Video BIOS - Set video mode
        mov     al, 04h                 ; CGA 320x200 4 color graphics mode
        int     10h

;------ Load map and show animation

        call    LoadMap                 ; Read and draw map from STDIN
        call    Animate                 ; Animate guard movements

;------ Print results to screen

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
        mov     ax, [count]             ; Convert [posY]
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
        mov     ax, 0C03h               ; Video - Draw white pixel
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

        mov     ax, 0C01h               ; Video - write cyan pixel
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
        mov     al, 02h                 ; Set pixel color to pink
        mov     [posX], cx              ; Save starting X position
        mov     [posY], dx              ; Save starting Y position
@@30:
        int     10h                     ; Call BIOS to write pixel
        jmp     @@10                    ; Loop to next char

@@40:
        mov     [mapWidth], cx          ; Save line width
        mov     ax, 0C03h               ; Video - write white pixel
        int     10h                     ; Call BIOS to draw border
        xor     cx, cx                  ; Reset X position to 0
        inc     dx                      ; Increment Y position
        int     10h                     ; Call Video BIOS
        jmp     @@10                    ; Loop

@@90:
        mov     [mapHeight], dx         ; Save Map height
        mov     cx, [mapWidth]          ; Prepare to draw [mapWidth] pixels
        mov     ax, 0C03h               ; Video - write white pixel
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
; Registers:
;       ax, bx, cx, dx, di, si
;---------------------------------------------------------------------
PROC    Animate

        mov     cx, [posX]      ; Load X position in CX
        mov     dx, [posY]      ; Load Y position in CX
        mov     bx, 00FFh       ; Load direction of movement up (0, -1)
        push    bx              ;  and save it to stack
        mov     [count], 1      ; Reset pink pixel counter
@@10:
        pop     bx              ; Restore direction of movement
        add     cl, bh          ; Compute next X position
        add     dl, bl          ; Compute next Y position
        push    bx              ; Save BX that may be trashed by BIOS calls
        mov     ah, 0Dh         ; Video BIOS - Read graphic pixel
        int     10h             ; Get pixel color in AL
        cmp     al, 3           ; Is it white?
        je      @@90            ;   yes, terminate
        cmp     al, 1           ; Is it cyan?
        je      @@20            ;   yes, turn right
        cmp     al, 2           ; Is it pink ?
        je      @@10            ;   yes, loop
        mov     ax, 0C02h       ; Video BIOS - write pink pixel
        int     10h             ; Call BIOS to draw pixel
        inc     [count]         ; Increment pixel count
        jmp     @@10            ; Continue animation
@@20:
        pop     bx              ; Restore current movement in BX
        sub     cl, bh          ; Revert movement
        sub     dl, bl
        neg     bl              ; 2-complement Y movement
        xchg    bl, bh          ; Swap X and Y movements
        push    bx              ; Save movement to stack
        jmp     @@10            ; Repeat movement

@@90:
        mov     ax, 0C02h       ; Video BIOS - write pink pixel
        int     10h             ; Call BIOS to draw pixel
        pop     bx              ; Restore movement

        ret                     ; Return to caller
ENDP    Animate



        END     Start           ; End of program / entry point
