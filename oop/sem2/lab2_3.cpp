#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Circle {
private:
    double x, y, radius;
public:
    Circle() {}

    Circle(double _x, double _y, double _radius) {
        x = _x;
        y = _y;
        radius = _radius;
    }

    double square() {
        return 3.14 * radius * radius;
    }

    double perimeter() {
        return 2 * 3.14 * radius;
    }

    double getX() const {
        return x;
    }

    double getY() const {
        return y;
    }

    double getRadius() {
        return radius;
    }

    bool isOnSameLineAs(Circle& other) const {
        return x == other.x || y == other.y;
    }

    string toString() {
        return "Circle: (" + to_string(x) + ", " + to_string(y) + "), r = " + to_string(radius) +
            "\nS = " + to_string(square()) + ". P = " + to_string(perimeter()) + "\n";
    }
};

int main() {
    vector<Circle> circles;

    circles.push_back(Circle(1, 2, 3));
    circles.push_back(Circle(2, 3, 4));
    circles.push_back(Circle(2, 16, 4));
    circles.push_back(Circle(3, 2, 5));
    circles.push_back(Circle(13, 5, 6));
    circles.push_back(Circle(5, 5, 10));
    circles.push_back(Circle(10, 15, 10));


    // Sort
    Circle min_sqr = circles[0], max_sqr = circles[0], min_per = circles[0], max_per = circles[0];
    for (auto circle : circles) {
        if (circle.square() < min_sqr.square())
            min_sqr = circle;
        if (circle.square() > max_sqr.square())
            max_sqr = circle;
        if (circle.perimeter() < min_per.perimeter())
            min_per = circle;
        if (circle.perimeter() > max_per.perimeter())
            max_per = circle;
    }

    cout << "Smallest circle by square:\n" << min_sqr.toString() << endl;
    cout << "Largest circle by square:\n" << max_sqr.toString() << endl;
    cout << "Smallest circle by perimeter:\n" << min_per.toString() << endl;
    cout << "Largest circle by perimeter:\n" << max_per.toString() << endl;

    // Find groups
    vector<vector<Circle>> groups;

    for (int i = 0; i < circles.size(); i++) {
        bool added = false;

        for (auto& group : groups) {
            if (group[0].isOnSameLineAs(circles[i])) {
                group.push_back(circles[i]);
                added = true;
                break;
            }
        }

        if (!added) {
            groups.push_back({circles[i]});
        }
    }

    cout << "Groups of circles whose centers lie on the same line:" << endl;
    for (int i = 0; i < groups.size(); i++) {
        cout << "Group " << i+1 << ": " << endl;
        for (auto& c : groups[i]) {
            cout << "(" << c.getX() << ", " << c.getY() << ")" << endl;
        }
    }
}