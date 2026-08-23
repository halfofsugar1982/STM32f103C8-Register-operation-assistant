void SystemInit(void)
{
	
}

void SysTick_Handler(void)
{
	* (unsigned int*) 0x4001080C=~(* (unsigned int*) 0x4001080C);
	* (unsigned int*) 0x4001100C=~(* (unsigned int*) 0x4001100C);	
}


int main(void)
{

	* (unsigned int*) 0x40021018 = 0x00000014;
	
	* (unsigned int*) 0x40011004 = 0x44344444;	
	* (unsigned int*) 0x40010800 = 0x44444443;
	
	* (unsigned int*) 0x4001080C = 0x00000001;	
	* (unsigned int*) 0x4001100C = 0x00002000;

	* (unsigned int*) 0xE000E014 = 7999999;
	* (unsigned int*) 0xE000E010 = 0x00000007;

	while(1);	
}
