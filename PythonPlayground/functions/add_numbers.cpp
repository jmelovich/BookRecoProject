#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

extern "C" {
    EXPORT double add_numbers(double a, double b) {
        return a + b;
    }
}

// This file demonstrates one method to define a C function in a usable way in Python
// To actually use this file, it must be compiled first into a dll
// In this example, I used the command:
// g++ -shared PythonPlayground/functions/add_numbers.cpp -o PythonPlayground/functions/add_numbers.dll
// This uses minGW to compile this file into a DLL file that is then loaded by the functions.py file