//
// Copyright 2015 riteme
//

#ifndef RILOG_FORMATTER_HPP_
#define RILOG_FORMATTER_HPP_

#include <string>

#include "Message.hpp"
#include "FormatConfig.hpp"

namespace ri {

class Formatter {
 public:
    virtual ~Formatter();

    virtual auto Format(const Message &message) const -> std::string = 0;

    void SetConfig(FormatConfig *config);
    auto GetConfig() const -> FormatConfig;

    void SetDateFormat(const std::string &format);
    void SetDateBufferSize(const std::size_t size);
    void SetMessageFormat(const std::string &format);
    void SetFieldName(const std::string &name);
    void SetThreadName(const std::thread::id &id, const std::string &name);
    void SetCurrentThreadName(const std::string &name);

 protected:
    FormatConfig m_default;
    FormatConfig *m_pConfig = &m_default;
};  // class Formatter

}  // namespace ri

#endif  // RILOG_FORMATTER_HPP_
