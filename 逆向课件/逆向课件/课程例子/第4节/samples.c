__attribute__((cdecl)) int a1(int a, int b, int c, int d, int e, int f, int g, int h)
{
    return a + b + c + d;
}


__attribute__((fastcall)) int a2(int a, int b, int c, int d, int e, int f, int g, int h)
{
    return a + b + 2*c + d;
}

__attribute__((stdcall)) int a3(int a, int b, int c, int d, int e, int f, int g, int h)
{
    return 3*a + 2*b + 2*c + d;
}

int main()
{
    int a, b, c, d, e, f, g, h;
    a = 10;
    b = 20;
    c = 30;
    d = 40;
    f = 0;
    g = 0;
    h = 0;
    e = 0;
    a1(a, b, c, d, e, f, g, h);
    a2(a, b, c, d, e, f, g, h);
    a3(a, b, c, d, e, f, g, h);
    return 0;
}