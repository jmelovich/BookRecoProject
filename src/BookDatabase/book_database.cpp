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
#include <unordered_set>

namespace py = pybind11;

// experimenting with Eigen for now
using DataFrame = Eigen::MatrixXd;


class BookEntry {
private:
    std::string title;
    std::vector<std::string> author;
    std::vector<std::string> genre;
    std::string description;
    std::string isbn;
    std::string image_link;
    std::string link;
    int year;
    int rating_count;
    int page_count;
    float rating;
    float price;

    std::vector<float> embedding; // the semantic embedding of the book description + title

public:
    BookEntry(const std::string& title, const std::vector<std::string>& author, const std::vector<std::string>& genre, const std::string& description,
              const std::string& isbn, const std::string& image_link, int year = -1, int rating_count = -1, int page_count = -1,
              float rating = -1.0, float price = -1.0, const std::string& link = "", const std::vector<float>& embedding = {}) :
              title(title), author(author), genre(genre), description(description), isbn(isbn), image_link(image_link),
              year(year), rating_count(rating_count), page_count(page_count), rating(rating), price(price), link(link), embedding(embedding) {}

    // Getters
    std::string getTitle() const { return title; }
    std::string getDescription() const { return description; }
    std::string getIsbn() const { return isbn; }
    std::string getImageLink() const { return image_link; }
    std::string getLink() const { return link; }
    int getYear() const { return year; }
    int getRatingCount() const { return rating_count; }
    int getPageCount() const { return page_count; }
    float getRating() const { return rating; }
    float getPrice() const { return price; }
    std::vector<float> getEmbedding() const { return embedding; }

    std::vector<std::string> getAuthors() const { return author; }
    std::string getAuthor() const {
        std::string result = "";
        for (const auto& a : author) {
            result += a + ", ";
        }
        return result;
    }

    std::vector<std::string> getGenres() const { return genre; }
    std::string getGenre() const {
        std::string result = "";
        for (const auto& g : genre) {
            result += g + ", ";
        }
        return result;
    }

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


// Helper function for computing additional variable swaps that occur during shell sort
void Shell_Helper(std::vector<BookEntry*>& books, int iteration, int current){
    if(current - iteration >= 0){
        if(books[current]->getRating() > books[current - iteration]->getRating()){
            BookEntry* temp = books[current];
            books[current] = books[current  - iteration];
            books[current - iteration] = temp;
            Shell_Helper(books, iteration, current - iteration);
        }
    }
}


// Shell sort algorithm for sorting books by rating in descending order
void Shell_Sort(std::vector<BookEntry*> &books, const std::string& sortBy = "rating"){
    // sortBy can be the following values:
    // "rating", "review_count", "num_pages", "title"
    int size = books.size();
    int iteration = size / 2;
    while(iteration > 0){
        for(int i = 0; i < size; i++){
            if(i + iteration < size){
                if(books[i + iteration]->getRating() > books[i]->getRating()){
                    BookEntry* temp = books[i];
                    books[i] = books[i + iteration];
                    books[i + iteration] = temp;
                    Shell_Helper(books, iteration, i);
                }
            }
        }
        iteration = iteration / 2;
    }
}


// Helper function to perform the quick sort algorithm recursively
// Sorts the book objects in descending order based on rating
void Quick_Helper(std::vector<BookEntry*>& Updated_books, std::vector<BookEntry*>& books){
    int size = books.size();
    std::vector<BookEntry*> leftlist;
    std::vector<BookEntry*> rightlist;
    BookEntry* pivot = books[size - 1];
    for (int i = 0; i < size - 1; i++){
        if (books[i]->getRating() >= pivot->getRating()){ // Flipped the sign to fix the "Descending" order
            leftlist.push_back(books[i]);
        }
        else if (books[i]->getRating() < pivot->getRating()){ // Flipped the sign to fix the "Descending" order
            rightlist.push_back(books[i]);
        }
    }
    if (leftlist.size() > 0){
        Quick_Helper(Updated_books, leftlist);
    }
    Updated_books.push_back(pivot);
    if (rightlist.size() > 0){
      Quick_Helper(Updated_books, rightlist);
    }
}


// Quick Sort function that returns a new vector of class objects sorted by rating in decending order.
void Quick_Sort(std::vector<BookEntry*>& books, const std::string& sortBy = "rating"){
    std::vector<BookEntry*> Updated_books;
    Quick_Helper(Updated_books, books);
    books = Updated_books;
}



// I used slides 90 from 6-Sorting as reference
void merge(std::vector<BookEntry*>& books, int left, int mid, int right){
    int n1 = mid - left + 1;
    int n2 = right - mid;
    std::vector<BookEntry*> left_books;
    std::vector<BookEntry*> right_books;

    for (int i = 0; i < n1; i++){
        left_books.push_back(books[left + i]);
    };
    for (int j = 0; j < n2; j++){
        right_books.push_back(books[mid + 1 + j]);
    };

    int i = 0;
    int j = 0;
    int k = left;
    while(i < n1 && j < n2){
        if (left_books[i]->getRating() >= right_books[j]->getRating()){ // LUKE: I added getRating() here because you can't compare BookEntry objects directly
            books[k] = left_books[i];
            i++;
        }
        else{
            books[k] = right_books[j];
            j++;
        }
        k++;
    }
    while(i < n1){
        books[k] = left_books[i];
        i++;
        k++;
    }
    while(j < n2){
        books[k] = right_books[j];
        j++;
        k++;
    }
}

// I used slides 89 from 6-Sorting as reference
void Merge_Sort(std::vector<BookEntry*>& books, int left, int right, const std::string& sortBy = "rating"){
    if (left < right){
        int mid = left + (right - left) /2;
        Merge_Sort(books, left, mid);
        Merge_Sort(books, mid+1, right);

        merge(books, left, mid, right);
    }
}


// helper functions
void trim(std::string& str) {
    str.erase(0, str.find_first_not_of(" \t\n\r\f\v"));
    str.erase(str.find_last_not_of(" \t\n\r\f\v") + 1);
}

// csv file has format: author,bookformat,desc,genre,img,isbn,isbn13,link,pages,rating,reviews,title,totalratings
auto parseCSVLine = [](const std::string& line) -> std::vector<std::string> {
    std::vector<std::string> fields;
    std::string field;
    bool inQuotes = false;

    for (size_t i = 0; i < line.length(); ++i) {
        if (line[i] == '"') {
            if (inQuotes && i + 1 < line.length() && line[i + 1] == '"') {
                // Handle escaped quotes within a quoted field
                field += '"';
                ++i;
            } else {
                // Toggle the inQuotes state
                inQuotes = !inQuotes;
            }
        } else if (line[i] == ',' && !inQuotes) {
            // Comma outside quotes signifies a new field
            fields.push_back(field);
            field.clear();
        } else {
            // Regular character or comma inside quotes
            field += line[i];
        }
    }
    fields.push_back(field); // Add the last field

    // Trim whitespace from each field
    for (auto& f : fields) {
        trim(f);
    }

    return fields;
};

auto safeStoi = [](const std::string& str, int defaultVal, auto trim) -> int {
    try {
        if (str.empty()) return defaultVal;
        trim(const_cast<std::string&>(str));
        return std::stoi(str);
    } catch (...) {
        return defaultVal;
    }
};

auto safeStof = [](const std::string& str, float defaultVal, auto trim) -> float {
    try {
        if (str.empty()) return defaultVal;
        trim(const_cast<std::string&>(str));
        return std::stof(str);
    } catch (...) {
        return defaultVal;
    }
};

auto splitString = [](const std::string& str) -> std::vector<std::string> {
    std::vector<std::string> result;
    std::istringstream ss(str);
    std::string token;
    while (std::getline(ss, token, ',')) {
        trim(token);
        result.push_back(token);
    }
    return result;
};


////////////////////////////////////////////////////////////////////
// CLASS DEFINITIONS ///////////////////////////////////////////////
////////////////////////////////////////////////////////////////////





// Abstract base class
class BookDatabase {
public:
    BookDatabase(const std::string& file_path) : file_path_(file_path) {
        py::module_ utils = py::module_::import("src.BookDatabase.book_utils");  // book_utils.py should contain your function
        python_function_ = utils.attr("get_text_embedding");
    }
    virtual ~BookDatabase() = default;

    // Abstract methods
    virtual std::map<std::string, std::vector<py::object>> findBooks(const std::map<std::string, std::string>& parameters) = 0;
    virtual bool loadDataFromDisk(const std::string& file_path, const int depth = -1) = 0;
    virtual std::vector<BookEntry*> filterBooks(const std::map<std::string, std::string>& parameters, const bool exclusive = true) = 0;

protected:
    std::string file_path_;
    py::object python_function_;
};

class BookDatabase_Type0 : public BookDatabase {
public:
    BookDatabase_Type0(const std::string& file_path, const int depth = -1) : BookDatabase(file_path) {
        bool loadedData = loadDataFromDisk(file_path, depth);
        if (!loadedData) {
            throw std::runtime_error("Failed to load data from disk");
        }
    }

    std::map<std::string, std::vector<py::object>> findBooks(const std::map<std::string, std::string>& parameters) override {
        std::vector<BookEntry*> filtered_books = filterBooks(parameters);
        sortBooks(filtered_books, parameters);
        return convertToDataFrame(filtered_books);
    }

    bool loadDataFromDisk(const std::string& file_path, const int depth = -1) override {
        book_data_.clear();
        genre_book_map.clear();

        std::ifstream file(file_path);
        if (!file.is_open()) {
            std::cerr << "Could not open file..." << std::endl;
            return false;
        }

        std::string line;
        std::getline(file, line); // Skip the header line

        int index = 0;
        std::string temp_line;
        while (std::getline(file, line)) {
            try {
                // Handle potential multi-line fields within quotes
                while (line.find('"') != std::string::npos && std::count(line.begin(), line.end(), '"') % 2 != 0) {
                    std::string next_line;
                    if (!std::getline(file, next_line)) break;
                    line += "\n" + next_line;
                }

                auto fields = parseCSVLine(line);

                if (fields.size() < 13) {
                    std::cerr << "Line " << index + 1 << " has insufficient fields" << std::endl;
                    continue;
                }else if (fields.size() > 13) {
                    std::cerr << "Line " << index + 1 << " has too many fields" << std::endl;
                    continue;
                }

                std::string author = fields[0];
                std::string bookformat = fields[1];
                std::string desc = fields[2];
                std::string genre = fields[3];
                std::string img = fields[4];
                std::string isbn = fields[5];
                std::string isbn13 = fields[6];
                std::string link = fields[7];

                int page_count = safeStoi(fields[8], -1, trim);
                float rating_value = safeStof(fields[9], -1.0f, trim);
                int review_count = safeStoi(fields[10], -1, trim);
                std::string title = fields[11];
                int rating_count = safeStoi(fields[12], -1, trim);

                std::vector<std::string> genres = splitString(genre);
                std::vector<std::string> authors = splitString(author);

                trim(title);
                trim(desc);
                trim(link);

                BookEntry entry(title, authors, genres, desc, isbn, img, -1, rating_count, page_count, rating_value, -1.0, link);
                book_data_.push_back(entry);

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

        if (book_data_.empty()) {
            throw std::runtime_error("No valid book entries were loaded");
            return false;
        }

        for (int i = 0; i < book_data_.size(); i++) {
            for (const auto& g : book_data_[i].getGenres()) {
                if (genre_book_map.find(g) == genre_book_map.end()) {
                    genre_book_map[g] = std::vector<BookEntry*>(1, &book_data_[i]);
                } else {
                    genre_book_map[g].push_back(&book_data_[i]);
                }
            }
        }

        return true;
    }

    std::vector<BookEntry*> filterBooks(const std::map<std::string, std::string>& parameters, const bool exclusive = true) {
        std::unordered_set<BookEntry*> unique_books;
        std::vector<std::string> genres;

        for (const auto& [key, value] : parameters) {
            if (key == "genre") {
                genres = splitString(value);
            }
        }

        if (exclusive) {
            bool first = true;
            for (const auto& g : genres) {
                if (genre_book_map.find(g) != genre_book_map.end()) {
                    if (first) {
                        unique_books.insert(genre_book_map[g].begin(), genre_book_map[g].end());
                        first = false;
                    } else {
                        std::unordered_set<BookEntry*> temp_set;
                        for (auto book : genre_book_map[g]) {
                            if (unique_books.find(book) != unique_books.end()) {
                                temp_set.insert(book);
                            }
                        }
                        unique_books = std::move(temp_set);
                    }
                }
            }
        } else {
            for (const auto& g : genres) {
                if (genre_book_map.find(g) != genre_book_map.end()) {
                    unique_books.insert(genre_book_map[g].begin(), genre_book_map[g].end());
                }
            }
        }

        // Convert the unordered_set back to vector
        return std::vector<BookEntry*>(unique_books.begin(), unique_books.end());
    }


    void sortBooks(std::vector<BookEntry*>& filtered_books, const std::map<std::string, std::string>& parameters){
        std::string sortMethod = "quick";
        std::string sortBy = "rating";
        bool ascending = false;
        for (const auto& [key, value] : parameters) {
            if (key == "sortMethod") {
                sortMethod = value;
            }
            if (key == "sortOrder") {
                ascending = value == "asc";
            }
            if (key == "sortBy") {
                sortBy = value;
            }
        }
        if(sortMethod == "quick"){
            Quick_Sort(filtered_books, sortBy); // doesn't seem to work at the moment
        }else if(sortMethod == "shell"){
            Shell_Sort(filtered_books, sortBy);
        }else if(sortMethod == "merge"){
            Merge_Sort(filtered_books, 0, filtered_books.size() - 1, sortBy);
        }else{
            std::cerr << "Invalid sort method" << std::endl;
            return;
        }
        // if ascending is true, we will reverse the order of filtered_books
        // this means the sort functions should sort in descending order
        if(ascending){
            std::reverse(filtered_books.begin(), filtered_books.end());
        }
    }

private:
    // declare a vector of BookEntry object
    // this will be used to store the data from the csv file
    // the vector will be sorted by rating
    std::vector<BookEntry> book_data_;
   
    // we will also declare a map of strings (genre) to vectors of integers (indices in the book_data_ list)
    // there can be multiple genres per book, so there can be multiple entries in the map for a single book
    std::map<std::string, std::vector<BookEntry*>> genre_book_map;

    std::map<std::string, std::vector<py::object>> convertToDataFrame(const std::vector<BookEntry*>& book_entries) {
        std::map<std::string, std::vector<py::object>> data;
        //author,bookformat,desc,genre,img,isbn,isbn13,link,pages,rating,reviews,title,totalratings
        for (const auto& entry : book_entries) {
            data["title"].push_back(py::str(entry->getTitle()));
            data["author"].push_back(py::cast(entry->getAuthors()));
            data["genre"].push_back(py::cast(entry->getGenres()));
            data["description"].push_back(py::str(entry->getDescription()));
            data["isbn"].push_back(py::str(entry->getIsbn()));
            data["img"].push_back(py::str(entry->getImageLink()));
            data["year"].push_back(py::int_(entry->getYear()));
            data["rating_count"].push_back(py::int_(entry->getRatingCount()));
            data["page_count"].push_back(py::int_(entry->getPageCount()));
            data["rating"].push_back(py::float_(entry->getRating()));
            data["price"].push_back(py::float_(entry->getPrice()));
            data["link"].push_back(py::str(entry->getLink()));
        }

        return data;
    }


};


PYBIND11_MODULE(book_database_cpp, m) {
    m.doc() = "C++ implementation of BookDatabase using pybind11";

    // Bind the abstract base class
    py::class_<BookDatabase, std::shared_ptr<BookDatabase>>(m, "BookDatabase")
        .def("findBooks", &BookDatabase::findBooks)
        .def("loadDataFromDisk", &BookDatabase::loadDataFromDisk)
        .def("filterBooks", &BookDatabase::filterBooks);

    // Bind the concrete implementation
    py::class_<BookDatabase_Type0, BookDatabase, std::shared_ptr<BookDatabase_Type0>>(m, "BookDatabase_Type0")
        .def(py::init<const std::string&>())
        .def(py::init<const std::string&, int>());
}