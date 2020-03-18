#include <stdio.h>
#include <omp.h>

#define N 1024*1024*128
int data[N];

void do_stuff(int part, int parts) {
	int idx, block = N / parts;
	for (idx = block * part; idx < block * part + block; idx++) {
		data[idx] = omp_get_thread_num();	
	}
}

void do_stuff_afraid(int part, int parts) {
	int idx, block = N / parts;
#pragma omp critical
	for (idx = block * part; idx < block * part + block; idx++) {
		data[idx] = omp_get_thread_num();	
	}
}

void lock_contention() {
	int i;
	double start, end;

	printf("Running test without synchronization\n\n");
	for (i = 1; i < 8; i *= 2) {
		omp_set_num_threads(i);
		start = omp_get_wtime();
#pragma omp parallel
		do_stuff(omp_get_thread_num(), i);
		end = omp_get_wtime();
		printf("%d threads ended in %.3lf ms\r\n", i, (end - start) * 1000);		
	}

	printf("\r\nRunning test with synchronization\n\n");
	for (i = 1; i < 8; i *= 2) {
		omp_set_num_threads(i);
		start = omp_get_wtime();
#pragma omp parallel
		do_stuff_afraid(omp_get_thread_num(), i);
		end = omp_get_wtime();
		printf("%d threads ended in %.3lf ms\r\n", i, (end - start) * 1000);		
	}
}


int main() {
	lock_contention();
}