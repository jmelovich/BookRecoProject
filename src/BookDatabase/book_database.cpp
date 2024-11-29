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
#include <iomanip>

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
        // First concatenate the title and description
       // std::string text = title + " :\n" + description;
        std::string text = title;

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
void Shell_Helper(std::vector<BookEntry*>& books, int iteration, int current, const std::string& sortBy = "rating"){
    if(sortBy == "rating"){
        if(current - iteration >= 0){
            if(books[current]->getRating() > books[current - iteration]->getRating()){
                BookEntry* temp = books[current];
                books[current] = books[current  - iteration];
                books[current - iteration] = temp;
                Shell_Helper(books, iteration, current - iteration, sortBy);
            }
        }
    }
    else if(sortBy == "title"){
        if(current - iteration >= 0){
            if(books[current]->getTitle() > books[current - iteration]->getTitle()){
                BookEntry* temp = books[current];
                books[current] = books[current  - iteration];
                books[current - iteration] = temp;
                Shell_Helper(books, iteration, current - iteration, sortBy);
            }
        }
    }
    else if(sortBy == "num_pages"){
        if(current - iteration >= 0){
            if(books[current]->getPageCount() > books[current - iteration]->getPageCount()){
                BookEntry* temp = books[current];
                books[current] = books[current  - iteration];
                books[current - iteration] = temp;
                Shell_Helper(books, iteration, current - iteration, sortBy);
            }
        }
    }
    else if(sortBy == "review_count"){
        if(current - iteration >= 0){
            if(books[current]->getRatingCount() > books[current - iteration]->getRatingCount()){
                BookEntry* temp = books[current];
                books[current] = books[current  - iteration];
                books[current - iteration] = temp;
                Shell_Helper(books, iteration, current - iteration, sortBy);
            }
        }
    }
}


// Shell sort algorithm for sorting books by rating in descending order
void Shell_Sort(std::vector<BookEntry*> &books, const std::string& sortBy = "rating"){
    // sortBy can be the following values:
    // "rating", "review_count", "num_pages", "title"
    int size = books.size();
    int iteration = size / 2;
    if(sortBy == "rating"){
        while(iteration > 0){
            for(int i = 0; i < size; i++){
                if(i + iteration < size){
                    if(books[i + iteration]->getRating() > books[i]->getRating()){
                        BookEntry* temp = books[i];
                        books[i] = books[i + iteration];
                        books[i + iteration] = temp;
                        Shell_Helper(books, iteration, i, sortBy);
                    }
                }
            }
            iteration = iteration / 2;
        }
    }
    else if(sortBy == "title"){
        while(iteration > 0){
            for(int i = 0; i < size; i++){
                if(i + iteration < size){
                    if(books[i + iteration]->getTitle() > books[i]->getTitle()){
                        BookEntry* temp = books[i];
                        books[i] = books[i + iteration];
                        books[i + iteration] = temp;
                        Shell_Helper(books, iteration, i, sortBy);
                    }
                }
            }
            iteration = iteration / 2;
        }
    }
    else if(sortBy == "num_pages"){
        while(iteration > 0){
            for(int i = 0; i < size; i++){
                if(i + iteration < size){
                    if(books[i + iteration]->getPageCount() > books[i]->getPageCount()){
                        BookEntry* temp = books[i];
                        books[i] = books[i + iteration];
                        books[i + iteration] = temp;
                        Shell_Helper(books, iteration, i, sortBy);
                    }
                }
            }
            iteration = iteration / 2;
        }
    }
    else if(sortBy == "review_count"){
        while(iteration > 0){
            for(int i = 0; i < size; i++){
                if(i + iteration < size){
                    if(books[i + iteration]->getRatingCount() > books[i]->getRatingCount()){
                        BookEntry* temp = books[i];
                        books[i] = books[i + iteration];
                        books[i + iteration] = temp;
                        Shell_Helper(books, iteration, i, sortBy);
                    }
                }
            }
            iteration = iteration / 2;
        }
    }
}


// Helper function to perform the quick sort algorithm recursively
// Sorts the book objects in descending order based on rating
void Quick_Helper(std::vector<BookEntry*>& Updated_books, std::vector<BookEntry*>& books, const std::string& sortBy = "rating"){
    int size = books.size();
    std::vector<BookEntry*> leftlist;
    std::vector<BookEntry*> rightlist;
    BookEntry* pivot = books[size - 1];
    if (sortBy == "rating"){
        for (int i = 0; i < size - 1; i++){
            if (books[i]->getRating() >= pivot->getRating()){ // Flipped the sign to fix the "Descending" order
                leftlist.push_back(books[i]);
            }
            else if (books[i]->getRating() < pivot->getRating()){ // Flipped the sign to fix the "Descending" order
                rightlist.push_back(books[i]);
            }
        }
    }
    else if (sortBy == "title"){
        for (int i = 0; i < size - 1; i++){
            if (books[i]->getTitle() >= pivot->getTitle()){ // Flipped the sign to fix the "Descending" order
                leftlist.push_back(books[i]);
            }
            else if (books[i]->getTitle() < pivot->getTitle()){ // Flipped the sign to fix the "Descending" order
                rightlist.push_back(books[i]);
            }
        }
    }
    else if (sortBy == "num_pages"){
        for (int i = 0; i < size - 1; i++){
            if (books[i]->getPageCount() >= pivot->getPageCount()){ // Flipped the sign to fix the "Descending" order
                leftlist.push_back(books[i]);
            }
            else if (books[i]->getPageCount() < pivot->getPageCount()){ // Flipped the sign to fix the "Descending" order
                rightlist.push_back(books[i]);
            }
        }
    }
     else if (sortBy == "review_count"){
        for (int i = 0; i < size - 1; i++){
            if (books[i]->getRatingCount() >= pivot->getRatingCount()){ // Flipped the sign to fix the "Descending" order
                leftlist.push_back(books[i]);
            }
            else if (books[i]->getRatingCount() < pivot->getRatingCount()){ // Flipped the sign to fix the "Descending" order
                rightlist.push_back(books[i]);
            }
        }
    }
    if (leftlist.size() > 0){
        Quick_Helper(Updated_books, leftlist, sortBy);
    }
    Updated_books.push_back(pivot);
    if (rightlist.size() > 0){
      Quick_Helper(Updated_books, rightlist, sortBy);
    }
}


// Quick Sort function that returns a new vector of class objects sorted by rating in decending order.
void Quick_Sort(std::vector<BookEntry*>& books, const std::string& sortBy = "rating"){
    std::vector<BookEntry*> Updated_books;
    Quick_Helper(Updated_books, books, sortBy);
    books = Updated_books;
}



// I used slides 90 from 6-Sorting as reference
void merge(std::vector<BookEntry*>& books, int left, int mid, int right, const std::string& sortBy = "rating"){
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
        if (sortBy == "rating"){
            if (left_books[i]->getRating() >= right_books[j]->getRating()){
                books[k] = left_books[i];
                i++;
            }
            else{
                books[k] = right_books[j];
                j++;
            }
        }
        else if (sortBy == "title"){
            if (left_books[i]->getTitle() >= right_books[j]->getTitle()){
                books[k] = left_books[i];
                i++;
            }
            else{
                books[k] = right_books[j];
                j++;
            }
        }
        else if (sortBy == "num_pages"){
            if (left_books[i]->getPageCount() >= right_books[j]->getPageCount()){
                books[k] = left_books[i];
                i++;
            }
            else{
                books[k] = right_books[j];
                j++;
            }
        }
        else if (sortBy == "review_count"){
            if (left_books[i]->getRatingCount() >= right_books[j]->getRatingCount()){
                books[k] = left_books[i];
                i++;
            }
            else{
                books[k] = right_books[j];
                j++;
            }
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
        Merge_Sort(books, left, mid, sortBy);
        Merge_Sort(books, mid+1, right, sortBy);

        merge(books, left, mid, right, sortBy);
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

// Function that takes in a vector of vectors of floats and writes them to a file
void writeEmbeddingsToFile(const std::vector<std::vector<float>>& embeddings, const std::string& file_path) {
    std::ofstream outfile(file_path);
    if (!outfile.is_open()) {
        std::cerr << "Failed to open file for writing" << std::endl;
        return;
    }

    // Set precision for floating-point numbers
    outfile << std::fixed << std::setprecision(10);

    for (const auto& emb : embeddings) {
        for (size_t i = 0; i < emb.size(); ++i) {
            outfile << emb[i];
            if (i < emb.size() - 1) {
                outfile << ",";
            }
        }
        outfile << std::endl;
    }

    // Explicitly close the file
    outfile.close();
}

// Function that reads embeddings from a file and returns a vector of vectors of floats
std::vector<std::vector<float>> readEmbeddingsFromFile(const std::string& file_path) {
    std::vector<std::vector<float>> embeddings;
    std::ifstream infile(file_path);
    if (!infile.is_open()) {
        std::cerr << "Failed to open file for reading" << std::endl;
        return embeddings;
    }

    std::string line;
    while (std::getline(infile, line)) {
        std::vector<float> emb;
        std::istringstream ss(line);
        std::string token;
        while (std::getline(ss, token, ',')) {
            try {
                emb.push_back(std::stof(token));
            } catch (const std::invalid_argument& e) {
                std::cerr << "Invalid float format: " << token << std::endl;
            }
        }
        embeddings.push_back(emb);
    }

    // Explicitly close the file
    infile.close();

    return embeddings;
}


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

    virtual bool getEmbeddings(const std::string &file_path)  = 0; // this function should attempt to load the embeddings from a file, if not it should generate them
    virtual void vectorSearch(const std::string& query, std::vector<BookEntry*> &books_input) = 0; // this function should return books sorted based on the cosine similarity of the query vector with the book embeddings

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
        // get the embeddings path from the file_path
        // the embeddings path should be the file_path with the file extension removed and "_embeddings.csv" appended
        embeddingsPath = file_path.substr(0, file_path.find_last_of('.')) + "_embeddings.csv";
    }

    void vectorSearch(const std::string& query, std::vector<BookEntry*>& books_input) override {

        // load the embeddings
        getEmbeddings(embeddingsPath);

        // Calculate the embedding for the query
        py::object embedding = python_function_(query);
        std::vector<float> embedding_vector = embedding.cast<std::vector<float>>();

        // Check if valid
        if (embedding_vector.empty()) {
            std::cout << "Invalid embedding for query" << std::endl;
            return; // Early exit if embedding is invalid
        }

        std::cout << "Calculated embedding for query: " << query << std::endl;

        // Calculate cosine similarity and store in a vector of pairs
        std::vector<std::pair<float, int>> similarity_scores;
        for (size_t i = 0; i < books_input.size(); ++i) {
            const auto& book_embedding = books_input[i]->getEmbedding();

            // Calculate dot product and magnitudes
            float dot_product = 0, query_magnitude = 0, book_magnitude = 0;
            for (size_t j = 0; j < embedding_vector.size(); ++j) {
                dot_product += embedding_vector[j] * book_embedding[j];
                query_magnitude += embedding_vector[j] * embedding_vector[j];
                book_magnitude += book_embedding[j] * book_embedding[j];
            }
            
            query_magnitude = std::sqrt(query_magnitude);
            book_magnitude = std::sqrt(book_magnitude);

            // Calculate cosine similarity
            float cosine_similarity = dot_product / (query_magnitude * book_magnitude);
            similarity_scores.emplace_back(cosine_similarity, i);
        }

        // Sort by cosine similarity in descending order
        std::sort(similarity_scores.begin(), similarity_scores.end(), std::greater<>());

        // Create a sorted vector of BookEntry pointers
        std::vector<BookEntry*> top_books;
        for (const auto& score : similarity_scores) {
            top_books.push_back(books_input[score.second]);
        }

        // Update the input vector with the sorted books
        books_input = std::move(top_books);
    }


    bool getEmbeddings(const std::string &file_path) override {
        // check if the file exists at file_path
        // if it does, load the embeddings from the file
        // if it doesn't, calculate the embeddings for each book and save them to the file
        // return true if successful, false otherwise

        if(embeddingsLoaded){
            std::cout << "Embeddings already loaded" << std::endl;
            return true;
        }else{
            std::cout << "Embeddings not already loaded, attempting to load from file" << std::endl;
        }

        if(file_path.empty()){
            std::cerr << "No file path provided" << std::endl;
            return false;
        }

        std::ifstream infile(file_path);
        if (infile.good()) {
            // file exists
            std::cout << "File exists" << std::endl;
            std::vector<std::vector<float>> embeddings = readEmbeddingsFromFile(file_path);
            // check if the number of embeddings matches the number of books
            if(embeddings.size() != book_data_.size()){
                std::cerr << "Number of embeddings doesn't match number of books" << std::endl;
                return false;
            }
            // set the embeddings for each book
            for (int i = 0; i < book_data_.size(); i++) {
                book_data_[i].setEmbedding(embeddings[i]);
            }
            std::cout << "Embeddings loaded from file" << std::endl;
            embeddingsLoaded = true;
            return true;
        }else{
            // file doesn't exist, so we will calculate the embeddings for each book
            // and save them to the file
            std::cout << "File doesn't exist, generating embeddings..." << std::endl;
            // create a variable to store the embeddings, this will be written to the file once all embeddings are calculated
            std::vector<std::vector<float>> embeddings;
            for (int i = 0; i < book_data_.size(); i++) {
                if (!book_data_[i].calculateEmbedding(python_function_)) {
                    std::cerr << "Failed to calculate embedding for book " << i << std::endl;
                    return false;
                }else{
                    std::cout << "Embedding calculated for book " << i << std::endl;
                    embeddings.push_back(book_data_[i].getEmbedding());
                }
            }
            // write the embeddings to the file
            writeEmbeddingsToFile(embeddings, file_path);
            std::cout << "Embeddings written to file" << std::endl;
            embeddingsLoaded = true;
            return true;
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

        bool isFiltered = false;

        for (const auto& [key, value] : parameters) {
            if (key == "genre") {
                genres = splitString(value);
                if(!genres.empty()){
                    isFiltered = true;
                }
            }
        }

        if (!isFiltered) {
            // if no filters are applied, return all books
            // create a vector of pointers to the book entries
            std::vector<BookEntry*> books;
            for (auto& entry : book_data_) {
                books.push_back(&entry);
            }
            return books;
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
        std::string vector_query = "";
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
            if (key == "search_terms") {
                vector_query = value;
            }
        }

        if(sortBy == "vector_search"){
            if(vector_query.empty()){
                std::cerr << "No query provided for vector search" << std::endl;
                return;
            }
            vectorSearch(vector_query, filtered_books);
        }else if(sortMethod == "quick"){
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

    bool embeddingsLoaded = false; // will be flipped to true once the embeddings are loaded
    std::string embeddingsPath = "embeddings.csv"; // default path for the embeddings file

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
        .def("filterBooks", &BookDatabase::filterBooks)
        .def("getEmbeddings", &BookDatabase::getEmbeddings)
        .def("vectorSearch", &BookDatabase::vectorSearch);

    // Bind the concrete implementation
    py::class_<BookDatabase_Type0, BookDatabase, std::shared_ptr<BookDatabase_Type0>>(m, "BookDatabase_Type0")
        .def(py::init<const std::string&>())
        .def(py::init<const std::string&, int>());
}