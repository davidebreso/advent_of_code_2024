{************ ADVENT OF CODE -- DAY 1 -- PROBLEM 1 ************}
program Day01_01;

uses	Crt;

procedure Sort(var a: array of LongInt; n: Integer);
var
	i: Integer;
    tmp: LongInt;
    swapped: Boolean;
begin
	swapped := True;
    while swapped do
    begin
    	swapped := False;
        for i := 0 to n - 2 do
        begin
			if a[i] > a[i + 1] then
            begin
            	tmp := a[i];
                a[i] := a[i + 1];
                a[i + 1] := tmp;
                swapped := True;
            end;
        end;
    end;
end;

var
	n, i, j: Integer;
    a, b, dist:	LongInt;
    inFile:	Text;

    right, left: array[0..2000] of LongInt;

begin
	ClrScr;
    Assign(inFile, 'input1.txt');
    Reset(inFile);
    dist := 0;
    n := 0;
    while True do
    begin
    	Read(inFile, a, b);
        if Eof(InFile) then break;
        left[n] := a;
        right[n] := b;
        { WriteLn(left[n], '  ', right[n]); }
        Inc(n);
    end;
    Sort(left, n);
    Sort(right, n);
    dist := 0;
    for i := 0 to n - 1 do
		dist := dist + Abs(left[i] - right[i]);
    WriteLn(dist);
end.