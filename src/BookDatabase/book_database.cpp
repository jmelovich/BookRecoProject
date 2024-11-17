// this is the C++ implementation of the BookDatabase class using pybind11
// Here an abstract base class BookDatabase is defined
// currently there are just two virtual methods for testing, but it will need to be extended obviously


#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <string>
#include <Eigen/Core>
#include <Eigen/Dense>

namespace py = pybind11;

// experimenting with Eigen for now
using DataFrame = Eigen::MatrixXd;


// Abstract base class
class BookDatabase {
public:
    BookDatabase(const std::string& file_path) : file_path_(file_path) {}
    virtual ~BookDatabase() = default;

    // Abstract methods
    virtual DataFrame findBooks(const DataFrame& query) = 0;
    virtual std::string testFunc(const std::string& input) = 0;

protected:
    std::string file_path_;
};



// Concrete implementation for testing
class SimpleBookDatabase : public BookDatabase {
public:
    SimpleBookDatabase(const std::string& file_path) : BookDatabase(file_path) {}

    DataFrame findBooks(const DataFrame& query) override {
        // Placeholder implementation
        // Just returns a 2x2 matrix for testing
        DataFrame result(2, 2);
        result << 1.0, 2.0,
                  3.0, 4.0;
        return result;
    }

    std::string testFunc(const std::string& input) override {
        // Placeholder implementation
        return "Test function called with input: " + input;
    }
};

PYBIND11_MODULE(book_database_cpp, m) {
    m.doc() = "C++ implementation of BookDatabase using pybind11";

    // Bind the abstract base class
    py::class_<BookDatabase, std::shared_ptr<BookDatabase>>(m, "BookDatabase")
        .def("findBooks", &BookDatabase::findBooks)
        .def("testFunc", &BookDatabase::testFunc);

    // Bind the concrete implementation
    py::class_<SimpleBookDatabase, BookDatabase, std::shared_ptr<SimpleBookDatabase>>(m, "SimpleBookDatabase")
        .def(py::init<const std::string&>());
}