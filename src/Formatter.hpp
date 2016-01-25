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

    void SetConfig(const FormatConfig &config);
    auto GetConfig() const -> FormatConfig;

 protected:
    const FormatConfig *m_pConfig = nullptr;
};  // class Formatter

}  // namespace ri

#endif  // RILOG_FORMATTER_HPP_
