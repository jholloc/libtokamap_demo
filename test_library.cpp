#include <string>
#include <dlfcn.h>
#include <exception>
#include <iostream>
#include <filesystem>

int main(int argc, char** argv)
{
    if (argc != 2) {
        std::cout << "usage: " << argv[0] << " library" << std::endl;
        return 1;
    }

    std::string file_name = argv[1];
    auto library_path = std::filesystem::absolute(file_name);

    if (!std::filesystem::exists(library_path)) {
        std::cerr << "Library '" << library_path.string() << "' does not exist" << std::endl;
        return 1;
    }

    void* handle = dlopen(library_path.c_str(), RTLD_LAZY);
    if (handle == nullptr) {
        std::string err = dlerror();
        std::cerr << "Failed to load library '" + library_path.string() + "': " + err << std::endl;
        return 1;
    }

    std::string symbol_name = "LibTokaMapFactoryLoader";

    void* function_pointer = dlsym(handle, symbol_name.c_str());
    if (function_pointer == nullptr) {
        std::string err = dlerror();
        std::cerr << "Failed to load symbol '" + symbol_name + "': " + err << std::endl;
        return 1;
    }

    std::cout << "Library ok!" << std::endl;
}
