//
// Copyright 2015 riteme
//

#ifndef RILOG_CPPFORMAT_FORMATTER_HPP_
#define RILOG_CPPFORMAT_FORMATTER_HPP_

#include "Formatter.hpp"

namespace ri {

class CppformatFormatter : public Formatter {
 public:
    CppformatFormatter();
    virtual ~CppformatFormatter();

    virtual auto Format(const Message &message) const -> std::string;
};  // class CppformatFormatter

}  // namespace ri

#endif  // RILOG_CPPFORMAT_FORMATTER_HPP_
