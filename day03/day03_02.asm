%TITLE "Advent of Code 2024 -- Day 3 -- Problem 2"

        IDEAL

        MODEL   small
        STACK   256

cr      EQU     13              ; ASCII carriage return
lf      EQU     10              ; ASCII line feed


        DATASEG

exCode          DB      0

inFile          DW      0               ; Input file handle
oneByte         DB      0               ; File read buffer
state           DB      0               ; State of DFA
;-Transition table----DIGIT----ALPHA---STATE---------------------------
trans           DB      0,      'm'     ; 0: Search for 'm'
                DB      0,      'u'     ; 1: Search for 'u'
                DB      0,      'l'     ; 2: Search for 'l'
                DB      0,      '('     ; 3: Search for '('
                DB      4,      ','     ; 4: Search for X digit or ','
                DB      5,      ')'     ; 5: Search for Y digit or ')'
;----------------------------------------------------------------------
strDo           DB      'do()',0        ; String to search for 'do()'
ptrDo           DW      offset strDo    ; Pointer to next char to search
strDont         DB      'don''t()',0    ; String to search for "don't()"
ptrDont         DW      offset strDont  ; Pointer to next char to search
doMul           DB      1               ; 1: Mul enabled, 0: Mul disabled
intX            DW      0               ; First argument of mul(X,Y)
intY            DW      0               ; Second argument of mul(X,Y)
intZ            DW      0               ; High byte for X * Y
sumL            DW      0               ; Store sum of muls
sumH            DW      0               ;   as 32 bit integer

fileName        DB      'input3.txt',0   ; Input file name

        CODESEG

;------ From BINASC.OBJ
        EXTRN   BinToAscDec:Proc, BinToAscHex:Proc

;------ From STRING.OBJ
        EXTRN   StrWrite:Proc, NewLine:Proc

;------ From DISKERR.OBJ
        EXTRN   DiskErr:Proc

Start:

;------ Initialize and display notes if no parameters entered

        mov     ax, @data       ; Initalize DS to address
        mov     ds, ax          ;  of data segment
        mov     es, ax          ; Make ES=DS

;------ Attept to open the input file

        mov     dx, offset fileName     ; Address file name with ds:dx
        xor     al, al                  ; Specify read-only access
        mov     ah, 3Dh                 ; DOS Open-file function
        int     21h                     ; Open the input file
        jnc     @@10                    ; Continue if no error
        jmp     Errors                  ; Else jump to error handler

@@10:
        mov     [inFile], ax            ; Save input file handle

;------ At this point, the input file is open and its handle is stored
;       at [inFile].  The next step is to read from the input file and
;       print each byte to the console.

@@20:
        mov     ah, 3Fh                 ; DOS Read-file function
        mov     bx, [inFile]            ; Set bx to input file handle
        mov     cx, 1                   ; Specify one byte to read
        mov     dx, offset oneByte      ; Address buffer with ds:dx
        int     21h                     ; Call DOS to read from file
        jnc     @@30                    ; Jump if no error detected
        jmp     Errors                  ; Else jump to error handler
@@30:
        or      ax, ax                  ; Check for end of input file
        jz      @@40                    ; ax=0=end of file; jump
        call    DoTransition            ; Execute one transition of DFA
        jmp     @@20                    ; Repeat for next byte

;------ Print result

@@40:
        mov     dx, [sumH]              ; Move result to DX:AX
        mov     ax, [sumL]
        call    PrintLongInt            ; Print result
        call    NewLine                 ;   followed by newline

;------ Close the input file, witch is not strictly required as ending
;       the program via function 04Ch also closes all open files.

        mov     bx, [inFile]            ; Set bx to input file handle
        mov     ah, 3Eh                 ; DOS Close-file function
        int     21h                     ; Close input file
Exit:
        mov     ah, 04Ch                ; DOS function: exit program
        mov     al, [exCode]            ; Return exit code value
        int     21h                     ; Call DOS. Terminate program

;------ Instructions jump to there to handle any I/O errors, which
;       cause the program to end after displaying a message.

Errors:
        mov     [exCode], al            ; Save error code
        call    DiskErr                 ; Display error message
        jmp     Exit                    ; Exit program

%NEWPAGE
;---------------------------------------------------------------------
; DoTransition          Execute one transition of DFA
;---------------------------------------------------------------------
; Input:
;       [oneByte]       Next char to consume
;       [state]         Current state of DFA
;       [ptrDo], [ptrDont]      pointer to Do/Don't string
; Ouput:
;       [state]         Next state of DFA
;       [ptrDo], [ptrDont]      pointer to Do/Don't string
;       [intX], [intY]  Arguments of mul(X,Y)
;       [sumH], [sumL]  Updated by adding X * Y
; Registers:
;       ax, bx, cx, dx, di, si
;---------------------------------------------------------------------
PROC    DoTransition
        mov     dl, [oneByte]           ; Load input char in DL
        xor     bh, bh                  ; Zero high byte of BX
        mov     bl, [state]             ; Load state in BL
        shl     bl, 1                   ; Covert to word offset
        mov     ax, [word ptr trans + bx]  ; Load delta in AX
        xor     cx, cx                  ; Zero CX for later

;------ Search for Do/Don't string
        mov     di, [ptrDo]             ; DI points to next char in strDo
        mov     si, [ptrDont]           ; SI points to next char in strDont
        cmp     dl, 'd'                 ; Is current char == 'd' ?
        jne     @@01                    ;   No, jump
        mov     di, offset strDo + 1    ; next char will be 'o'
        mov     si, offset strDont + 1  ; next char will be 'o'
        jmp     @@80                    ; reset DFA state and terminate
@@01:
        cmp     dl, [di]                ; Match in strDo?
        jne     @@02                    ;   No, reset and check strDont
        inc     di                      ;   Yes, increment ptrDo
        jmp     @@03                    ; Go to check strDont
@@02:
        mov     di, offset strDo        ; reset PtrDo
@@03:
        cmp     dl, [si]                ; Match in ptrDont?
        jne     @@05                    ;   No, reset and check for digit
        inc     si                      ;   Yes, increment ptrDont
        jmp     @@80                    ; reset DFA state and terminate
@@05:
        mov     si, offset strDont      ; reset ptrDont
;------ Match with digit 0..9
        cmp     dl, '0'                 ; Is char < '0' ?
        jb      @@10                    ;   Yes, go to alpha match
        cmp     dl, '9'                 ; Is char > '9' ?
        ja      @@10                    ;   Yes, go to alpha match
        cmp     [intX], 100             ; Is [intX] a 3 digit number ?
        jae     @@10                    ;   Yes, go to alpha match
        mov     bl, al                  ; Match! Next state is in al
        sub     dl, '0'                 ; Convert char to number
        mov     cl, dl                  ;   and save it in CX
        mov     ax, 10                  ; Multiply IntX by 10
        mul     [intX]
        add     ax, cx                  ; Add digit to 10 * IntX
        mov     [intX], ax              ;   and save it to IntX
        jmp     @@90                    ; Go to end

;------ Match with alphabetic character
@@10:
        shr     bl, 1                   ; Restore state from word offset
        cmp     bl, 4                   ; Where we searching for X ?
        jb      @@40                    ;   Not yet
        ja      @@20                    ;   Too late, jump!
        push    ax                      ; Else save AX for later
        mov     ax, [intX]              ; Move [intX] to
        mov     [intY], ax              ;   [intY]
        pop     ax                      ; Restore AX
@@20:
        cmp     bl, 5                   ; Where we searching for Y ?
        jne     @@40                    ;   No, jump
        push    ax                      ; Save registers
        push    dx
        mov     ax, [intX]              ; Multiply [intX]
        mul     [intY]                  ;   with [intY]
        mov     [intY], ax              ; And save the result in [intZ]:[intY]
        mov     [intZ], dx
        pop     dx                      ; Restore registers
        pop     ax
@@40:
        mov     [intX], 0               ; Reset IntX to 0
        cmp     dl, 'm'                 ; Is current char 'm' ?
        jne     @@50                    ;   No, check for other symbols
        mov     bl, 1                   ; Else next state is 1
        jmp     @@90

@@50:
        cmp     dl, ah                  ; Is current char a match?
        jne     @@80                    ;   No, reset state to 0
        inc     bl                      ; Increment state
        cmp     bl, 6                   ; Is > 5 ?
        jne     @@90                    ;   No, go to end
        cmp     [doMul], 1              ; Are Muls enabled?
        jne     @@90                    ;   No, go to end
        mov     ax, [intY]              ;   Yes, add [intY] (low byte)
        add     [sumL], ax              ;     to [sumL]
        mov     ax, [intZ]              ; Add [intX] (high byte)
        adc     [sumH], ax              ;   to [sumH], with carry
@@80:
        xor     bx, bx                  ; Reset state to 0
@@90:
        cmp     [byte ptr di], 0                 ; End of strDo ?
        jne     @@95                    ;   no, jump
        mov     di, offset strDo        ;   yes, reset ptrDo
        mov     [doMul], 1              ; And enable Muls
@@95:
        cmp     [byte ptr si], 0                 ; End of strDont?
        jne     @@99                    ;   no, jump
        mov     si, offset strDont      ;   yes, reset ptrDo
        mov     [doMul], 0              ; And disable Muls
@@99:
        mov     [state], bl             ; Store next state
        mov     [ptrDo], di             ; Store next ptrDo
        mov     [ptrDont], si           ; Store next ptrDont
        ret                             ; Return to caller
ENDP    DoTransition
%NEWPAGE
;---------------------------------------------------------------------
; PrintLongInt          Print a 32 bit integer to screen
;---------------------------------------------------------------------
; Input:
;       DX:AX           32 bit integer to print
; Ouput:
;       print number to screen
; Registers:
;       ax, bx, cx, dx
;---------------------------------------------------------------------
PROC    PrintLongInt
        mov     bx, 10          ; Print as decimal number
        push    bx              ; Push sentinel to stack
@@10:
        mov     cx, ax          ; Temporarily store LowDividend in CX
        mov     ax, dx          ; First divide the HighDividend
        xor     dx, dx          ; Setup for division DX:AX / BX
        div     bx              ;  -> AX is HighQuotient, Reminder is reused
        xchg    ax, cx          ; Temp. move it to CX, restore LowDividend
        div     bx              ;  -> AX is LowQuotient, Reminder DX=[0,9]
        push    dx              ; Save reminder for now
        mov     dx, cx          ; Build true 32-bit quotient in DX:AX
        or      cx, ax          ; Is the true 32-bit quotient zero?
        jnz     @@10            ; No, use as next dividend
        pop     dx              ; First pop (is digit for sure)
@@20:
        add     dl, '0'         ; Turn into character
        mov     ah, 02h         ; DOS DisplayCharacter
        int     21h             ; Call DOS to display digit
        pop     dx              ; All remaining pops
        cmp     dx, bx          ; Was it the sentinel?
        jb      @@20            ; Not yet, loop
        ret                     ; Return to caller
ENDP    PrintLongInt

        END     Start           ; End of program / entry point
