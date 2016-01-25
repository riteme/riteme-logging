//
// Copyright 2015 riteme
//

#ifndef RILOG_LOG_TYPE_NAME_HPP_
#define RILOG_LOG_TYPE_NAME_HPP_

#include <string>
#include <unordered_map>

#include "LogType.hpp"

namespace ri {

static std::unordered_map<LogType, std::string> LOGTYPE = {
    { LogType::Unknown, "UNKNOWN" },
    { LogType::Debug, "DEBUG" },
    { LogType::Trace, "TRACE" },
    { LogType::Info, "INFO" },
    { LogType::Warning, "WARN" },
    { LogType::Error, "ERROR" },
    { LogType::Fatal, "FATAL" }
};

static std::unordered_map<LogType, std::string> logtype = {
    { LogType::Unknown, "Unknown" },
    { LogType::Debug, "Debug" },
    { LogType::Trace, "Trace" },
    { LogType::Info, "Info" },
    { LogType::Warning, "Warning" },
    { LogType::Error, "Error" },
    { LogType::Fatal, "Fatal" }
};

}  // namespace ri

#endif  // RILOG_LOG_TYPE_NAME_HPP_
