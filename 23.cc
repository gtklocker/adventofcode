#include <iostream>
#include <unordered_map>
#include <unordered_set>

using namespace std;

struct Cup {
	int val;
	Cup *next;
};

Cup* take(Cup *cup, int amount, bool print=false) {
	Cup *thisCup = cup;
	for (int i = 0; i < amount; ++i) {
		thisCup = thisCup->next;
		if (print) {
			cout << thisCup->val << (i < amount-1 ? ' ' : '\n');
		}
	}
	return thisCup;
}

int main() {
	Cup *head = nullptr;
	Cup *tip = nullptr;
	//string allCups = "389125467";
	string allCups = "123487596";
	unordered_map<int, Cup*> loc;
	int maxVal = 1e6;
	for (char c : allCups) {
		int val = c-'0';
		Cup *newCup = new Cup{val, nullptr};
		loc[val] = newCup;
		if (tip == nullptr) {
			head = tip = newCup;
		} else {
			tip->next = newCup;
			tip = newCup;
		}
	}
	for (int val = 10; val <= maxVal; ++val) {
		Cup *newCup = new Cup{val, nullptr};
		loc[val] = newCup;
		tip->next = newCup;
		tip = newCup;
	}
	tip->next = head;

	Cup *current = head;
	unordered_set<int> fours;
	const int STEPS = 1e7;
	for (int step = 0; step < STEPS; ++step, current = current->next) {
		Cup *threeLater = take(current, 3);

		Cup *oneOfFour = current;
		fours.clear();
		while (oneOfFour != threeLater->next) {
			fours.insert(oneOfFour->val);
			oneOfFour = oneOfFour->next;
		}

		int destination = current->val;
		while (fours.find(destination) != fours.end()) {
			if (--destination == 0) {
				destination = maxVal;
			}
		}
		Cup *destNext = loc[destination]->next;
		loc[destination]->next = current->next;
		current->next = threeLater->next;
		threeLater->next = destNext;
	}
	take(loc[1], 2, true);
}
