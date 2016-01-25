//
// Copyright 2015 riteme
//

#ifndef RILOG_WRITER_HPP_
#define RILOG_WRITER_HPP_

#include <mutex>
#include <string>

namespace ri {

class Writer {
 public:
    virtual ~Writer();

    virtual void Write(const std::string &buffer) = 0;
    virtual void Flush() = 0;

 protected:
    friend class Logger;

    auto _GetInnerLock() -> std::mutex &;

    std::mutex m_innerLock;
};  // class Writer

}  // namespace ri

#endif  // RILOG_WRITER_HPP_
