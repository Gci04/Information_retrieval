#include <stdio.h>
#include <stdint.h>

/* http://stackoverflow.com/a/9887979 */
/* http://stackoverflow.com/a/13628516 */
 __inline__ uint64_t rdtsc(void) {
	uint32_t lo, hi;
	__asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
	return (uint64_t)hi << 32 | lo;
}

void main() {
	unsigned long long en, st;
	printf("time start %llu ns\n", st = rdtsc());
	int i, x = 0;
	for (i = 0; i < 100000000; i++) {
		x += i - 6; x -= 7; x += 7;
	}
	printf("time end   %llu ns\n", en = rdtsc());
	printf("time total %llu ns\n", en - st);
	printf("time total %f s\n", (en - st + 0.0) / 1e9);
}