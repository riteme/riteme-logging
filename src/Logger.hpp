//
// Copyright 2015 riteme
//

#ifndef RILOG_LOGGER_HPP_
#define RILOG_LOGGER_HPP_

#include <string>
#include <vector>
#include <stdexcept>

#include "thirdparty/cppformat.hpp"

#include "LogType.hpp"
#include "Formatter.hpp"
#include "Writer.hpp"

namespace ri {

class Logger final {
 public:
    Logger() = default;
    ~Logger() = default;

    void AttachFormatter(Formatter *formatter) {
        m_pFormatter = formatter;
    }

    void AttachWriter(Writer *writer) {
        m_writers.push_back(writer);
    }

    void DetachFormatter() {
        m_pFormatter = nullptr;
    }

    void DetachWriter() {
        m_writers.clear();
    }

    void SetLevel(const LogType &level) {
        m_level = level;
    }

    auto GetLevel() const -> LogType {
        return m_level;
    }

    auto IsValid() const -> bool {
        return m_pFormatter != nullptr and m_writers.size() > 0;
    }

    template <typename... Args>
    void Log(const LogType &type, const std::string &formatted,
             const Args &... args) {
        if (!IsValid()) {
            throw std::runtime_error("Formatter or Writer not valid.");
        }

        if (static_cast<int>(type) < static_cast<int>(m_level)) {
            return;
        }

        Message message;
        message.LogType = type;
        time(&message.RawTime);
        message.Text = fmt::format(formatted, args...);
        message.ThreadID = std::this_thread::get_id();

        std::string buffer = m_pFormatter->Format(message);

        for (auto writer : m_writers) {
            std::lock_guard<std::mutex> guard(writer->_GetInnerLock());
            writer->Write(buffer);
            writer->Write("\n");
            writer->Flush();
        }  // foreach in m_writers
    }

    template <typename... Args>
    void Debug(const std::string &formatted, const Args &... args) {
        Log(LogType::Debug, formatted, args...);
    }

    template <typename... Args>
    void Trace(const std::string &formatted, const Args &... args) {
        Log(LogType::Trace, formatted, args...);
    }

    template <typename... Args>
    void Info(const std::string &formatted, const Args &... args) {
        Log(LogType::Info, formatted, args...);
    }

    template <typename... Args>
    void Warning(const std::string &formatted, const Args &... args) {
        Log(LogType::Warning, formatted, args...);
    }

    template <typename... Args>
    void Error(const std::string &formatted, const Args &... args) {
        Log(LogType::Error, formatted, args...);
    }

    template <typename... Args>
    void Fatal(const std::string &formatted, const Args &... args) {
        Log(LogType::Fatal, formatted, args...);
    }

 private:
    LogType m_level = LogType::Info;
    Formatter *m_pFormatter = nullptr;
    std::vector<Writer *> m_writers;
};  // class Logger

}  // namespace ri

#endif  // RILOG_LOGGER_HPP_
