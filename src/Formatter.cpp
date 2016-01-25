//
// Copyright 2015 riteme
//

#include "Formatter.hpp"

namespace ri {

Formatter::~Formatter() = default;

void Formatter::SetConfig(const FormatConfig &config) {
    m_pConfig = &config;
}

auto Formatter::GetConfig() const -> FormatConfig {
    return *m_pConfig;
}

}  // namespace ri
