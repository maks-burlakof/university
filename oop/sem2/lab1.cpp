#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    vector<string> numbers;
    double avgLength = 0;

    cout << "Enter numbers separated by spaces: ";
    string inputLine;
    getline(cin, inputLine);

    size_t pos = 0; // int
    string lineSubstr;
    while ((pos = inputLine.find(' ')) != string::npos) {
        lineSubstr = inputLine.substr(0, pos);
        numbers.insert(numbers.begin(), lineSubstr);
        avgLength += lineSubstr.length();
        inputLine.erase(0, pos + 1);
    }
    numbers.insert(numbers.begin(), inputLine);

    avgLength /= numbers.size();

    cout << "\nNumbers less than average length (" << avgLength << "):" << endl;
    for (const string& number : numbers)
        if (number.length() < avgLength)
            cout << number << " (" << number.length() << ")\n";

    cout << endl << "Numbers greater than average length (" << avgLength << "):" << endl;
    for (const string& n : numbers)
        if (n.length() > avgLength)
            cout << n << " (" << n.length() << ")\n";

    return 0;
}
