#include <iostream>
#include <fstream>
#include <string>
using namespace std;

string encrypt(string);
string decrypt(string);
string remove_comments(string);

int main() {
    ifstream input_file("input.txt");
    if (input_file.is_open()) {
        string input_data, line;
        while (getline(input_file, line)) {
            input_data = input_data + line + '\n';
        }
        input_file.close();
        cout << "Input text:\n" + input_data + '\n';
        string fixed_string = remove_comments(input_data);
        cout << "Removed comments:\n" + fixed_string + '\n';
        ofstream output_file("output.txt");
        if (output_file.is_open()) {
            string encrypted_string = encrypt(fixed_string);
            output_file << encrypted_string << "\n\n" << fixed_string;
            output_file.close();
            cout << "Encrypted string:\n" + encrypted_string + '\n';
            cout << "\nDecrypted string:\n" + decrypt(encrypted_string) + "\n";
        }
        else {
            cout << "Error: could not write to file.\n";
        }
    }
    else {
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

string remove_comments(string input) {
    string output = "";
    bool inSingleLineComment = false;
    bool inMultiLineComment = false;

    for (int i = 0; i < input.size(); i++) {
        if (inSingleLineComment) {
            if (input[i] == '\n') {
                inSingleLineComment = false;
                output += '\n';
            }
        }
        else if (inMultiLineComment) {
            if (input[i] == '*' && i < input.size() - 1 && input[i + 1] == '/') {
                inMultiLineComment = false;
                i++; // Skip the '/'
            }
        }
        else {
            if (input[i] == '/' && i < input.size() - 1) {
                if (input[i + 1] == '/') {
                    inSingleLineComment = true;
                    i++; // Skip the second '/'
                }
                else if (input[i + 1] == '*') {
                    inMultiLineComment = true;
                    i++; // Skip the '*'
                }
                else if (input[i + 1] == '*') {
                    inMultiLineComment = true;
                    i++; // Skip the second '*'
                }
                else {
                    output += input[i];
                }
            }
            else {
                output += input[i];
            }
        }
    }

    return output;
}