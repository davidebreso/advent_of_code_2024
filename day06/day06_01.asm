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
        push    es                      ; Save registers

        mov     ax, 0B800h              ; Set ES to
        mov     es, ax                  ;    CGA screen address
        mov     si, 2000h               ; ES:SI points to line 1
        mov     di, si                  ; ES:DI points to line 1
        mov     al, 03h                 ; Draw white pixel
        stosb

;------ Read Input from STDIN one line at a time
        mov     dx, offset buffer       ; DS:DX points to input buffer
        xor     bx, bx                  ; Zero line width counter
@@10:
        push    bx                      ; Save BX for later
        mov     ah, 3Fh                 ; DOS - Read from file
        mov     bx, 0                   ; STDIN file handle
        mov     cx, 4                   ; Read 4 chars
        int     21h                     ; Call DOS to read one line
        pop     bx                      ; Restore line width counter
        or      ax, ax                  ; Check if EOF
        jz      @@90                    ;   Terminate if EOF
        xor     ah, ah                  ; Zero pixels to draw
        push    si                      ; Save SI for later
        mov     si, offset buffer       ; DS:SI points to buffer
        mov     cx, 4                   ; draw 4 pixels
@@20:
        lodsb                           ; Load char in AL
        shl     ah, 1
        shl     ah, 1                   ; Shift pixel block by 2
        cmp     al, 0Dh                 ; Is it CR ?
        je      @@30                    ; Yes, go to line update
        cmp     al, '^'                 ; Found start point?
        jne     @@25                    ;   no, continue as normal
        or      ah, 02h                 ; Color pixel pink
        mov     [posX], bx              ; Save starting X position
        push    bx                      ; Save BX to stack
        mov     bx, [mapHeight]
        mov     [posY], bx              ; Save starting Y position
        pop     bx                      ; Restore BX
@@25:
        and     al, 001h                ; Keep only LSB
        or      ah, al                  ; Store pixel color
        inc     bx                      ; Increment line width counter
        loop    @@20
        mov     al, ah                  ; Set pixel colors
        stosb                           ; Draw 4 pixels
        pop     si                      ; Restore SI
        jmp     @@10                    ; Loop
@@30:
        or      ah, 03h                 ; Set white pixel
        dec     cl
        shl     ah, cl                  ; Shift reminder pixels
        shl     ah, cl
        mov     al, ah                  ; Set pixel colors
        stosb                           ; Draw 4 pixel
        pop     si                      ; Restore SI
        mov     [mapWidth], bx          ; save line width value to [width]
        xor     bx, bx                  ;   and reset line width counter
        inc     [mapHeight]             ; Increment number of lines

        xor     si, 02000h              ; Switch to other half of screen
        test    si, 02000h
        jnz     @@40                    ; Are we on the odd half?
        add     si, 80                  ;   No, add 80 byte to pointer
@@40:
        mov     di, si                  ; ES:DI points to start of next line
        mov     al, 03h                 ; Draw white border
        stosb
        jmp     @@10                    ; Loop

@@90:
        xor     di, di                  ; ES:DI points to start of screen
        mov     al, 03h                 ; White left border
        stosb
        xchg    di, si
        stosb                           ; Write white left border
        mov     ax, [mapWidth]          ; AX is line width
        xor     dx, dx                  ; Zero DX for division
        mov     bx, 4                   ; Divide by 4 to
        div     bx                      ;  convert to bytes (reminder in DX)
        mov     cx, ax                  ; converted to bytes
        push    cx                      ; Save CX for later
        mov     al, 0FFh                ; Write white horizontal line
        rep     stosb
        xchg    di, si
        pop     cx
        rep     stosb
        mov     cl, 3
        sub     cl, dl                  ; Compute last byte shift
        shl     al, cl
        shl     al, cl
        stosb
        xchg    di, si
        stosb

        pop     es                      ; Restore registers
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
        add     cx, 4           ; Convert to absolute screen position
        mov     dx, [posY]      ; Load Y position in CX
        inc     dx              ; Convert to absolute screen position
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
