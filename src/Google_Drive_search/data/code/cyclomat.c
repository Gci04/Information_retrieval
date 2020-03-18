#include <stdio.h>
#include <stdlib.h>

/* M = 19 - 14 + 2*1 = 7 */
void A(int argc, char **argv) {
	if (argc == 1) printf("A: no params\n");		
	else if (argc == 2) printf("B: one param, %s\n", argv[1]);
	else if (argc == 3) {
		int x = atoi(argv[1]);
		int y = atoi(argv[2]);
		if (x > y) printf("C: x > y\n");
		else printf("D: x <= y\n");
	} else {
		printf("E: More than 2 params\n");
	}
	
	if (argc > 1) {
		if (!strcmp(argv[1], "777")) {
			printf("F: JackPot!\n");
		} else {
			printf("G: :(\n");
		}
	}
}

/* M = 16 - 12 + 2*1 = 6 */
void B(int argc, char **argv) {
	int x, y;
	if (argc == 1) {
		 printf("A: no params\n");
	} else {
		switch (argc) {
			case 2: printf("B: one param, %s\n", argv[1]); break;
			case 3: 		
				x = atoi(argv[1]);
				y = atoi(argv[2]);
				if (x > y) printf("C: x > y\n");
				else 	printf("D: x <= y\n");
				break;
			default: printf("E: More than 2 params\n");
		}
		if (!strcmp(argv[1], "777")) printf("F: JackPot!\n");
		else printf("G: :(\n");
	}
}           

void main(int argc, char** argv) {
	A(argc, argv);
	B(argc, argv);
}
