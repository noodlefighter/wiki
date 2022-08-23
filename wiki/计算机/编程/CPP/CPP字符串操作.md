## CPP字符串转整型

```c++
	std::string y = "A8";
	int x;
 
	try {
		x = std::stol(y, nullptr, 16);
	}
	catch (std::invalid_argument&){		
		cout << "Invalid_argument" << endl;
	}
	catch (std::out_of_range&){
		cout << "Out of range" << endl;
	}
	catch (...) {		
		cout << "Something else" << endl;
	}

```

