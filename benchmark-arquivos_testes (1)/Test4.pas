program Test4;
var
   A, B, R, I : integer;

procedure teste (A:integer; B:real);

{verifique se é necessário um ";" no fechamento de um procedimento}

begin
   while (I <= 5) do
   begin
      A := A+1;
      B := B-1;
      R := A + B;
      I := I + 1;

      for I := 1 to 5 do
   begin
      A := A * A;
      B := B * A;
      R := A + B
   end
   end
end.

{retirar algumas palavras reservadas para gerar erros sintáticos}