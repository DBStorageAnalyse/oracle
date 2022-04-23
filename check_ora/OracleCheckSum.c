函数原型
unsigned short __stdcall OracleCheck(
	const char *pBuf,/*页缓冲区*/ 
	int PageSize/*页大小*/
	)
返回值：unsigend short （2字节无符号整数）


#include "stdio.h"

#define DLLEXPORT extern "C" __declspec(dllexport)

DLLEXPORT unsigned short __stdcall OracleCheck(const char *pBuf, int PageSize)
{
	unsigned short num = 0, ChkSum = 0;

	ChkSum = *(unsigned short*)pBuf;
	for(int i = 2; i < PageSize; i+=2)
	{
		num = *(unsigned short*)(pBuf+i);
		ChkSum ^= num;
	}
	return ChkSum;
}


