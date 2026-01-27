void __cdecl ValidateLocalCookies(void (__fastcall *cookieCheckFunction)(unsigned int), _EH4_SCOPETABLE *scopeTable, char *framePointer)
{
    unsigned int v3; // esi@2
    unsigned int v4; // esi@3

    if ( scopeTable->GSCookieOffset != -2 )
    {
        v3 = *(_DWORD *)&framePointer[scopeTable->GSCookieOffset] ^ (unsigned int)&framePointer[scopeTable->GSCookieXOROffset];
        __guard_check_icall_fptr(cookieCheckFunction);
        ((void (__thiscall *)(_DWORD))cookieCheckFunction)(v3);
    }
    v4 = *(_DWORD *)&framePointer[scopeTable->EHCookieOffset] ^ (unsigned int)&framePointer[scopeTable->EHCookieXOROffset];
    __guard_check_icall_fptr(cookieCheckFunction);
    ((void (__thiscall *)(_DWORD))cookieCheckFunction)(v4);
}

int __cdecl _except_handler4_common(unsigned int *securityCookies, void (__fastcall *cookieCheckFunction)(unsigned int), _EXCEPTION_RECORD *exceptionRecord, unsigned __int32 sehFrame, _CONTEXT *context)
{
    // 异或解密 scope table
    scopeTable_1 = (_EH4_SCOPETABLE *)(*securityCookies ^ *(_DWORD *)(sehFrame + 8));

    // sehFrame 等于 上图 ebp - 10h 位置, framePointer 等于上图 ebp 的位置
    framePointer = (char *)(sehFrame + 16);
    scopeTable = scopeTable_1;

    // 验证 GS
    ValidateLocalCookies(cookieCheckFunction, scopeTable_1, (char *)(sehFrame + 16));
    __except_validate_context_record(context);

    if ( exceptionRecord->ExceptionFlags & 0x66 )
    {
        ......
    }
    else
    {
        exceptionPointers.ExceptionRecord = exceptionRecord;
        exceptionPointers.ContextRecord = context;
        tryLevel = *(_DWORD *)(sehFrame + 12);
        *(_DWORD *)(sehFrame - 4) = &exceptionPointers;
        if ( tryLevel != -2 )
        {
            while ( 1 )
            {
                v8 = tryLevel + 2 * (tryLevel + 2);
                filterFunc = (int (__fastcall *)(_DWORD, _DWORD))*(&scopeTable_1->GSCookieXOROffset + v8);
                scopeTableRecord = (_EH4_SCOPETABLE_RECORD *)((char *)scopeTable_1 + 4 * v8);
                encloseingLevel = scopeTableRecord->EnclosingLevel;
                scopeTableRecord_1 = scopeTableRecord;
                if ( filterFunc )
                {
                    // 调用 FilterFunc
                    filterFuncRet = _EH4_CallFilterFunc(filterFunc);
                    ......
                    if ( filterFuncRet > 0 )
                    {
                        ......
                        // 调用 HandlerFunc
                        _EH4_TransferToHandler(scopeTableRecord_1->HandlerFunc, v5 + 16);
                        ......
                    }
                }
                ......
                tryLevel = encloseingLevel;
                if ( encloseingLevel == -2 )
                    break;
                scopeTable_1 = scopeTable;
            }
            ......
        }
    }
  ......
}