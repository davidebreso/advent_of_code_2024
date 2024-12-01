{************ ADVENT OF CODE -- DAY 1 -- PROBLEM 2 ************}
program Day01_02;

uses	Crt;

function Count(x: LongInt; a: array of LongInt; n: Integer): LongInt;
var
	i: Integer;
    res: LongInt;
begin
	res := 0;
	for i := 0 to n - 1 do
		if a[i] = x then
        	res := res + x;
	Count := res;
end;

var
	n, i: Integer;
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
        Inc(n);
    end;
    dist := 0;
    for i := 0 to n - 1 do
	begin
		dist := dist + Count(left[i], right, n);
    end;
    WriteLn(dist);
end.