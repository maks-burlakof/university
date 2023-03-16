#include <iostream>
#include <fstream>
#include <string>
using namespace std;

string encrypt(string input);
string decrypt(string input);
string fix_mistakes(string input);

int main() {
    ifstream input_file("../lab3text/input.txt");
    if (input_file.is_open()) {
        string original_string;
        getline(input_file, original_string);
        input_file.close();
        cout << "Original string: " + original_string + '\n';
        string corrected_str = fix_mistakes(original_string);
        cout << "Corrected string: " + corrected_str + '\n';
        ofstream output_file("../lab3text/output.txt");
        if (output_file.is_open()) {
            string encrypted_string = encrypt(corrected_str);
            output_file << encrypted_string << "\n" << corrected_str;
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

string fix_mistakes(string input) {
    string fixed_string;
    for (size_t i = 0; i < input.size(); i++) {
        if (i > 0 && tolower(input[i-1]) == 'p' && tolower(input[i]) == 'a' && isalpha(input[i+1])) {
            fixed_string += 'o';
        } else {
            fixed_string += input[i];
        }
    }
    return fixed_string;
}
