//
// Copyright 2015 riteme
//

#ifndef RILOG_CONSOLE_WRITER_HPP
#define RILOG_CONSOLE_WRITER_HPP

#include "Writer.hpp"

namespace ri {

class ConsoleWriter : public Writer {
 public:
    ConsoleWriter();
    virtual ~ConsoleWriter();

    virtual void Write(const std::string &buffer);
    virtual void Flush();
    virtual void SetSync(const bool flag);
};  // class ConsoleWriter

}  // namespace ri

#endif  // RILOG_CONSOLE_WRITER_HPP
