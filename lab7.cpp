//#include <iostream>
//using namespace std;
//int main()
//{
//    setlocale(LC_ALL, "Russian");
//    char s[81];
//    int lens = 0, leng = 0, pos = 0;
//    puts("Введите строку из групп нулей и единиц ");
//    gets_s(s);
//    while (s[lens] != '\0') lens++;
//    int lengm = lens;
//    for (int i = 0; i < lens; i++) {
//        if (s[i] != '1' && s[i] != '0') continue;
//        leng++;
//        if (s[i] != s[i + 1]) {
//            if (leng < lengm) {
//                lengm = leng;
//                pos = i - leng + 1;
//            }
//            leng = 0;
//        }
//    }
//    if (pos == 0 && lengm == lens) {
//        puts("Невозможно найти наименьшую группу");
//        return 0;
//    }
//    leng = 0;
//    int lengm_new = lens, pos_new = 0, sum = 0;
//    for (int i = lens-1; i >= pos + lengm; i--) {
//        if (s[i] != '1' && s[i] != '0') continue;
//        leng++;
//        if (s[i] != s[i - 1]) {
//            if (leng < lengm_new) {
//                lengm_new = leng;
//                pos_new = i;
//            }
//            leng = 0;
//        }
//        if (lengm_new == lengm) {
//            for (int i = pos_new; i < pos_new + lengm_new; i++) cout << s[i];
//            cout << "\n";
//            sum++;
//            lengm_new = lens;
//        }
//    }
//    for (int i = pos; i < pos + lengm; i++) cout << s[i];
//    if (sum > 0) cout << "\nНайдено групп: " << sum + 1 << "\n";
//    else cout << "\nНайдена одна наименьшая группа\n";
//    return 0;
//}
//
//// 111111110000000011111777000000
//// 00001110000111000011100001110000

#include <iostream>
using namespace std;
#define _CRT_SECURE_NO_WARNINGS
int main()
{
	char s[21], a[21];
	//scanf("%s", *s);
	printf("%s %s", s, a);
	return 0;
}