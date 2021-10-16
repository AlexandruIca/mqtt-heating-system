#include "log.hpp"
#include "mqtt_client.hpp"

auto main() -> int
{
    mqtt::setup_log();
    INFO("Hello {}!", "world");
    WARNING("Hello {}!", "world");
    ERROR("Hello {}!", "world");
}