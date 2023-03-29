#include <iostream>
#include <fstream>
#include <string>
using namespace std;

string encrypt(string);
string decrypt(string);
int count_words(const string&);
bool is_vowel(char);

int main() {
    ifstream input_file("../lab3text/input.txt");
    if (input_file.is_open()) {
        string original_string = "", line;
        while (getline(input_file, line))
            original_string = original_string + line + " ";
        input_file.close();
        cout << "Original string: " + original_string + '\n';

        int word_count = count_words(original_string);
        cout << "Number of words that begin and end with a vowel: " << word_count << endl;

        ofstream output_file("../lab3text/output.txt");
        if (output_file.is_open()) {
            string encrypted_string = encrypt(original_string);
            output_file << encrypted_string;
            output_file.close();
            cout << "Encrypted string: " + encrypted_string + '\n';
            cout << "Decrypted string: " + decrypt(encrypted_string) + "\n";
        } else {
            cout << "Error: could not write to file.\n";
        }
    } else {
        cout << "Error: could not read input file.\n";
    }
    return 0;
}

string encrypt(string input) {
    string encrypted_string;
    for (char c : input) {
        c += 3;
        encrypted_string += c;
    }
    return encrypted_string;
}

string decrypt(string input) {
    string decrypted_string;
    for (char c : input) {
        c -= 3;
        decrypted_string += c;
    }
    return decrypted_string;
}

char VOWEL_LIB[] = {'a', 'e', 'i', 'o', 'u'};

bool is_vowel(char c) {
     for (char vc : VOWEL_LIB)
         if (tolower(c) == vc)
             return true;
     return false;
}

int count_words(const string& line) {
    int count = 0;
    string word;

    for (char c : line) {
        if (c == ' ' || c == '\n' || c == '.' || c == ',' || c == ':') {
            if (!word.empty()) {
                if (is_vowel(word[0]) && is_vowel(word[word.length()-1])) {
                    count++;
                    // cout << word << ", ";
                }
                word = "";
            }
        } else {
            word += c;
        }
    }
    if (!word.empty()) {
        if (is_vowel(word[0]) && is_vowel(word[word.length()-1]))
            count++;
    }

    return count;
}