#ifndef LOGGER_HPP_
#define LOGGER_HPP_
#pragma once

#include <boost/current_function.hpp>
#include <boost/log/trivial.hpp>
#include <fmt/color.h>
#include <fmt/core.h>

#define LOGGER_LINE_FILLER(file, line, function, color)                                                                \
    color << fmt::format("[{}:{} <{}>]: \033[0m", file, line, function)

#define INFO(...)                                                                                                      \
    BOOST_LOG_TRIVIAL(info) << LOGGER_LINE_FILLER(__FILE__, __LINE__, BOOST_CURRENT_FUNCTION, "\033[32m")              \
                            << fmt::format(__VA_ARGS__)

#define WARNING(...)                                                                                                   \
    BOOST_LOG_TRIVIAL(warning) << LOGGER_LINE_FILLER(__FILE__, __LINE__, BOOST_CURRENT_FUNCTION, "\033[33m")           \
                               << fmt::format(__VA_ARGS__)

#define ERROR(...)                                                                                                     \
    BOOST_LOG_TRIVIAL(error) << LOGGER_LINE_FILLER(__FILE__, __LINE__, BOOST_CURRENT_FUNCTION, "\033[31m")             \
                             << fmt::format(__VA_ARGS__)

#endif