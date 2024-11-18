// this is the C++ implementation of the BookDatabase class using pybind11
// Here an abstract base class BookDatabase is defined
// currently there are just two virtual methods for testing, but it will need to be extended obviously


#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <string>
#include <Eigen/Core>
#include <Eigen/Dense>
#include <fstream>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>
#include <iostream>

namespace py = pybind11;

// experimenting with Eigen for now
using DataFrame = Eigen::MatrixXd;

class BookEntry {
private:
    std::string title;
    std::string author;
    std::string genre;
    std::string description;
    std::string isbn;
    std::string image_link;
    int year;
    int rating_count;
    int page_count;
    float rating;
    float price;

    std::vector<float> embedding; // the semantic embedding of the book description + title

public:
    BookEntry(const std::string& title, const std::string& author, const std::string& genre, const std::string& description,
              const std::string& isbn, const std::string& image_link, int year = -1, int rating_count = -1, int page_count = -1,
              float rating = -1.0, float price = -1.0, const std::vector<float>& embedding = {}) :
              title(title), author(author), genre(genre), description(description), isbn(isbn), image_link(image_link),
              year(year), rating_count(rating_count), page_count(page_count), rating(rating), price(price), embedding(embedding) {}

    // Getters
    std::string getTitle() const { return title; }
    std::string getAuthor() const { return author; }
    std::string getGenre() const { return genre; }
    std::string getDescription() const { return description; }
    std::string getIsbn() const { return isbn; }
    std::string getImageLink() const { return image_link; }
    int getYear() const { return year; }
    int getRatingCount() const { return rating_count; }
    int getPageCount() const { return page_count; }
    float getRating() const { return rating; }
    float getPrice() const { return price; }
    std::vector<float> getEmbedding() const { return embedding; }

    // Setters
    void setEmbedding(const std::vector<float>& embedding) { this->embedding = embedding; }

    bool calculateEmbedding(py::object python_function_) {
        // TODO: Implement actual embedding calculation
        // This can be done one of two ways:
        // 1. Calculate the embedding using a local model
        //    -- This would probably be easier to program in python and then call from C++
        // 2. Call a remote service to calculate the embedding
        //    -- This would require making an HTTP request to the OpenAI endpoint
        //    -- This is probably the better option, as I can run a local inference server anyway

        // I will implement the second option for now

        // First concatenate the title and description
        std::string text = title + " :\n" + description;

        // Call the python function to get the text embedding
        py::object embedding = python_function_(text);

        // Convert the embedding to a vector of floats
        std::vector<float> embedding_vector = embedding.cast<std::vector<float>>();

        // if valid, set the embedding
        if (embedding_vector.size() > 0) {
            this->embedding = embedding_vector;
        } else {
            return false;
        }

        return true;
    }


};


// Abstract base class
class BookDatabase {
public:
    BookDatabase(const std::string& file_path) : file_path_(file_path) {
        py::module_ utils = py::module_::import("src.BookDatabase.book_utils");  // book_utils.py should contain your function
        python_function_ = utils.attr("get_text_embedding");
    }
    virtual ~BookDatabase() = default;

    // Abstract methods
    virtual DataFrame findBooks(const DataFrame& query) = 0;
    virtual bool loadDataFromDisk(const std::string& file_path, const int depth = -1) = 0;

    virtual std::string testFunc(const std::string& input) = 0;
    virtual std::string printBooks(const int depth) = 0;

protected:
    std::string file_path_;
    py::object python_function_;
};



// Concrete implementation for testing
class SimpleBookDatabase : public BookDatabase {
public:
    SimpleBookDatabase(const std::string& file_path, const int depth = -1) : BookDatabase(file_path) {
        bool loadedData = loadDataFromDisk(file_path, depth);
        if (!loadedData) {
            throw std::runtime_error("Failed to load data from disk");
        }
    }

    DataFrame findBooks(const DataFrame& query) override {
        // Placeholder implementation
        // Just returns a 2x2 matrix for testing
        DataFrame result(2, 2);
        result << 1.0, 2.0,
                  3.0, 4.0;
        return result;
    }

    bool loadDataFromDisk(const std::string& file_path, const int depth = -1) override {
        // this method needs to be modified because the genre field can hold multiple values
        // this implementation assumes one genre per book

        std::vector<BookEntry> book_data_temp;
        std::map<std::string, std::vector<int>> genre_indices_temp;

        std::ifstream file(file_path);
        if (!file.is_open()) {
            throw std::runtime_error("Could not open file");
            return false;
        }

        std::string line;
        std::getline(file, line); // Skip the header line

        auto parseCSVLine = [](const std::string& line) -> std::vector<std::string> {
            std::vector<std::string> fields;
            std::string field;
            bool inQuotes = false;
            
            for (size_t i = 0; i < line.length(); ++i) {
                if (line[i] == '"') {
                    if (i + 1 < line.length() && line[i + 1] == '"') {
                        // Handle escaped quotes
                        field += '"';
                        ++i;
                    } else {
                        inQuotes = !inQuotes;
                    }
                } else if (line[i] == ',' && !inQuotes) {
                    fields.push_back(field);
                    field.clear();
                } else {
                    field += line[i];
                }
            }
            fields.push_back(field); // Don't forget the last field
            return fields;
        };

        auto trim = [](std::string& str) {
            str.erase(0, str.find_first_not_of(" \t\n\r\f\v"));
            str.erase(str.find_last_not_of(" \t\n\r\f\v") + 1);
        };

        auto safeStoi = [trim](const std::string& str, int defaultVal = -1) -> int {
            try {
                if (str.empty()) return defaultVal;
                trim(const_cast<std::string&>(str));
                return std::stoi(str);
            } catch (...) {
                return defaultVal;
            }
        };

        auto safeStof = [trim](const std::string& str, float defaultVal = -1.0f) -> float {
            try {
                if (str.empty()) return defaultVal;
                trim(const_cast<std::string&>(str));
                return std::stof(str);
            } catch (...) {
                return defaultVal;
            }
        };

        int index = 0;
        while (std::getline(file, line)) {
            try {
                auto fields = parseCSVLine(line);
                
                // Ensure we have enough fields
                if (fields.size() < 13) {
                    std::cerr << "Line " << index + 1 << " has insufficient fields" << std::endl;
                    continue;
                }

                // Extract fields with proper trimming
                std::string author = fields[0];
                std::string bookformat = fields[1];
                std::string desc = fields[2];
                std::string genre = fields[3];
                std::string img = fields[4];
                std::string isbn = fields[5];
                std::string isbn13 = fields[6];
                std::string link = fields[7];
                
                // Convert numeric fields safely
                int page_count = safeStoi(fields[8]);
                float rating_value = safeStof(fields[9]);
                int review_count = safeStoi(fields[10]);
                std::string title = fields[11];
                int rating_count = safeStoi(fields[12]);

                // Trim text fields
                trim(author);
                trim(genre);
                trim(title);
                trim(desc);

                // Create book entry and add to temporary storage
                BookEntry entry(title, author, genre, desc, isbn, img, -1, rating_count, page_count, rating_value, -1.0);
                book_data_temp.push_back(entry);
                genre_indices_temp[genre].push_back(index);
                index++;

                if (depth > 0 && index >= depth) {
                    break;
                }
            }
            catch (const std::exception& e) {
                std::cerr << "Error processing line " << index + 1 << ": " << e.what() << std::endl;
                continue;
            }
        }

        file.close();

        // Only proceed if we have valid data
        if (book_data_temp.empty()) {
            throw std::runtime_error("No valid book entries were loaded");
            return false;
        }

        // Sort books within each genre by rating
        for (auto& [genre, indices] : genre_indices_temp) {
            std::sort(indices.begin(), indices.end(), [&book_data_temp](int a, int b) {
                return book_data_temp[a].getRating() > book_data_temp[b].getRating();
            });
        }

        // Flatten the sorted book_data_temp into book_data_
        int total_index = 0;
        for (const auto& [genre, indices] : genre_indices_temp) {
            genre_indices_[genre] = {total_index, total_index + indices.size() - 1};
            for (int index : indices) {
                book_data_.push_back(book_data_temp[index]);
                total_index++;
            }
        }

        return true;
    }

    std::string testFunc(const std::string& input) override {
        // Placeholder implementation
        return "Test function called with input: " + input;
    }

    std::string printBooks(const int depth) override {
        // Placeholder implementation
        // Just print the first 'depth' books
        std::string output = "";
        for (int i = 0; i < depth; i++) {
            output += "Genre: " + book_data_[i].getGenre() + ", Rating: " + std::to_string(book_data_[i].getRating()) + ", Title: " + book_data_[i].getTitle() + "\n";
        }
        return output;
    }

private:
    // declare a vector of BookEntry object
    // this will be used to store the data from the csv file
    // the vector will be grouped by genre and sorted by rating
    std::vector<BookEntry> book_data_;
   
    // we will also declare a map of strings (genre) to pairs of integers
    // where the integers are the start and end indices of the genre in the book_data_ vector
    // this will allow us to quickly find the range of indices for a given genre
    std::map<std::string, std::pair<int, int>> genre_indices_;
};

PYBIND11_MODULE(book_database_cpp, m) {
    m.doc() = "C++ implementation of BookDatabase using pybind11";

    // Bind the abstract base class
    py::class_<BookDatabase, std::shared_ptr<BookDatabase>>(m, "BookDatabase")
        .def("findBooks", &BookDatabase::findBooks)
        .def("testFunc", &BookDatabase::testFunc)
        .def("loadDataFromDisk", &BookDatabase::loadDataFromDisk)
        .def("printBooks", &BookDatabase::printBooks);

    // Bind the concrete implementation
    py::class_<SimpleBookDatabase, BookDatabase, std::shared_ptr<SimpleBookDatabase>>(m, "SimpleBookDatabase")
        .def(py::init<const std::string&>())
        .def(py::init<const std::string&, int>());

    // Bind the BookEntry class
    // py::class_<BookEntry, std::shared_ptr<BookEntry>>(m, "BookEntry")
    //     .def(py::init<const std::string&, const std::string&, const std::string&, const std::string&, const std::string&, const std::string&,
    //                   int, int, int, float, float, const std::vector<float>&>())
    //     .def("getTitle", &BookEntry::getTitle)
    //     .def("getAuthor", &BookEntry::getAuthor)
    //     .def("getGenre", &BookEntry::getGenre)
    //     .def("getDescription", &BookEntry::getDescription)
    //     .def("getIsbn", &BookEntry::getIsbn)
    //     .def("getImageLink", &BookEntry::getImageLink)
    //     .def("getYear", &BookEntry::getYear)
    //     .def("getRatingCount", &BookEntry::getRatingCount)
    //     .def("getPageCount", &BookEntry::getPageCount)
    //     .def("getRating", &BookEntry::getRating)
    //     .def("getPrice", &BookEntry::getPrice)
    //     .def("getEmbedding", &BookEntry::getEmbedding)
    //     .def("setEmbedding", &BookEntry::setEmbedding)
    //     .def("calculateEmbedding", &BookEntry::calculateEmbedding);
}