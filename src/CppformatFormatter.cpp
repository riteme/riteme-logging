//
// Copyright 2015 riteme
//

#include <ctime>

#include "thirdparty/cppformat.hpp"

#include "LogTypeName.hpp"
#include "CppformatFormatter.hpp"

namespace ri {
CppformatFormatter::CppformatFormatter() = default;
CppformatFormatter::~CppformatFormatter() = default;

auto CppformatFormatter::Format(const Message &message) const -> std::string {
    struct tm *timeinfo = std::localtime(&message.RawTime);
    char buffer[m_pConfig->DateBufferSize];

    strftime(buffer, m_pConfig->DateBufferSize, m_pConfig->DateFormat.data(),
             timeinfo);
    std::string date = buffer;

    return fmt::format(m_pConfig->MessageFormat, "date"_a = date,
                       "field"_a = m_pConfig->FieldName,
                       "thread"_a = m_pConfig->ThreadMap.at(message.ThreadID),
                       "logtype"_a = logtype[message.LogType],
                       "LOGTYPE"_a = LOGTYPE[message.LogType],
                       "text"_a = message.Text);
}

}  // namespace ri
