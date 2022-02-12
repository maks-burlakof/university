#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <stdio.h>
#include <conio.h>
#include <io.h>
using namespace std;

struct TZap {
	char f_name[21], l_name[21], y_birth[5], g_num[10];
	int m_phys, m_math, m_inf, m_chem;
	double s_b;
} Zap;
FILE *inp, *out, *indiv;
char File_In[] = "zapisi.dat", File_Out[] = "rezult.txt", File_Indiv[] = "zadanie.txt";
void Out(TZap &, FILE *);

int main() {
	//setlocale(LC_ALL, "Russian");
	int size = sizeof(TZap), i, kol, needed;
	long len;
	char letter;
	TZap st, *mas_Z;
	while (true) {
		puts("\n---------\n1 - Create new file\n2 - Add\n3 - View\n4 - Edit\n5 - Individual task\n0 - EXIT");
		char ch = _getch();
		system("cls");
		switch (ch) {
		case '1':
			puts("\nDo you want to create a new file?\nAll your data will be lost!\nPress 1 to continue");
			if (_getch() != '1') {
				puts("\n\n   Operation canceled");
				break;
			}
			inp = fopen(File_In, "wb");
			if (inp == NULL) {
				puts("\n   Create ERROR!");
				return 0;
			}
			fclose(inp);
			printf("\n   Created new file %s !\n", File_In);
			break;
		case '2':
			inp = fopen(File_In, "ab");
			fflush(stdin);
			printf("\nFirst name: ");
			scanf("%s", Zap.f_name);
			printf("\nLast name: ");
			scanf("%s", Zap.l_name);
			printf("\nYear of birth: ");
			scanf("%s", Zap.y_birth);
			printf("\nGroup number: ");
			scanf("%s", Zap.g_num);
			printf("\nGrades in physics, math, computer science, chemistry (space-separated): ");
			scanf("%i %i %i %i", &Zap.m_phys, &Zap.m_math, &Zap.m_inf, &Zap.m_chem);
			printf("\nAvg mark: ");
			Zap.s_b = (Zap.m_phys + Zap.m_math + Zap.m_inf + Zap.m_chem) / 4.;
			printf("%6.3lf", Zap.s_b);
			fwrite(&Zap, size, 1, inp);
			fclose(inp);
			puts("\nSuccess!");
			break;
		case '3':
			out = fopen(File_Out, "w");
			if ((inp = fopen(File_In, "rb")) == NULL) {
				puts("\n   Open ERROR!");
				return 0;
			}
			while (fread(&Zap, size, 1, inp)) Out(Zap, out);
			fclose(inp);
			fclose(out);
			break;
		case '4':
			inp = fopen(File_In, "r+b");
			cout << "What's student? Enter number: ";
			cin >> needed;
			fseek(inp, size * (needed - 1), 0);
			fflush(stdin);
			printf("\nFirst name: ");
			scanf("%s", st.f_name);
			printf("\nLast name: ");
			scanf("%s", st.l_name);
			printf("\nYear of birth: ");
			scanf("%s", st.y_birth);
			printf("\nGroup - ");
			scanf("%s", st.g_num);
			printf("\nGrades in physics, math, computer science, chemistry (space-separated): ");
			scanf("%i %i %i %i", &st.m_phys, &st.m_math, &st.m_inf, &st.m_chem);
			printf("\nAvg mark: ");
			st.s_b = (st.m_phys + st.m_math + st.m_inf + st.m_chem) / 4.;
			printf("%6.3lf", st.s_b);
			puts("\n\n   Editing menu is closed\n");
			fwrite(&st, size, 1, inp);
			fclose(inp);
			break;
		case '5':
			inp = fopen(File_In, "rb");
			indiv = fopen(File_Indiv, "w");
			len = _filelength(_fileno(inp));
			kol = len / size;
			mas_Z = new TZap[kol];
			fread(mas_Z, size, kol, inp);
			fclose(inp);
			puts("Search:\nEnter letter: ");
			cin >> letter;
			fprintf(indiv, "\t-- Personal data of excellent students --\n\n");
			for (i = 0; i < kol; i++) {
				if (mas_Z[i].f_name[0] == letter && mas_Z[i].s_b >= 8) Out(mas_Z[i], indiv);
			} // Критерий отличника - оценка >= 8
			delete[]mas_Z;
			fclose(indiv);
			break;
		case '0':
			return 0;
		default:
			break;
		}
	}
}

void Out(TZap &z, FILE* name) {
	printf("Name: %s %s\nYear of birth: %s\nGroup number: %s\nGrades: %i %i %i %i\nAvg mark: %6.3lf\n\n", z.f_name, z.l_name, z.y_birth, z.g_num, z.m_phys, z.m_math, z.m_inf, z.m_chem, z.s_b);
	fprintf(name, "Name: %s %s\nYear of birth: %s\nGroup number: %s\nGrades: %i %i %i %i\nAvg mark: %6.3lf\n\n", z.f_name, z.l_name, z.y_birth, z.g_num, z.m_phys, z.m_math, z.m_inf, z.m_chem, z.s_b);
}