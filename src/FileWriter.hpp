//
// Copyright 2015 riteme
//

#ifndef RILOG_FILE_WRITER_HPP_
#define RILOG_FILE_WRITER_HPP_

#include <fstream>

#include "Writer.hpp"

namespace ri {

class FileWriter : public Writer {
 public:
    FileWriter();
    FileWriter(const std::string &file);
    virtual ~FileWriter();

    virtual void Write(const std::string &buffer);
    virtual void Flush();

    virtual void Open(const std::string &file);
    virtual void Close();
    virtual auto IsOpened() const -> bool;

 private:
    std::ofstream m_file;
};  // class FileWriter

}  // namespace ri

#endif  // RILOG_FILE_WRITER_HPP_
