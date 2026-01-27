__attribute__((cdecl)) int a1(int a, int b, int c, int d)
{
    return a + b + c + d;
}


__attribute__((fastcall)) int a2(int a, int b, int c, int d)
{
    return a + b + 2*c + d;
}

__attribute__((stdcall)) int a3(int a, int b, int c, int d)
{
    return 3*a + 2*b + 2*c + d;
}

int main()
{
    int a, b, c, d;
    a = 10;
    b = 20;
    c = 30;
    d = 40;
    a1(a, b, c, d);
    a2(a, b, c, d);
    a3(a, b, c, d);
    return 0;
}