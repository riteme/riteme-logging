//
// Copyright 2015 riteme
//

#include <thread>
#include <chrono>

#include <rilog/Logging.hpp>
#include <rilog/FileWriter.hpp>

using namespace std;
using namespace std::chrono;
using namespace ri;

void output(FormatConfig *config, Logger *logger, int id) {
    config->SetThreadName(fmt::format("Thread #{}", id));

    logger->SetLevel(LogType::Debug);
    logger->Debug("Hello!");
    logger->Info("Thread started.");

    auto start = high_resolution_clock::now();
    int i = 0;
    while (i < 3) {
        logger->Info("Running...");
        this_thread::sleep_for(milliseconds(500));

        auto end = high_resolution_clock::now();
        auto t = duration_cast<milliseconds>(end - start).count();
        logger->Debug("Time passed: {}", t);
        i++;

        if (i == 3) {
            logger->Warning("This thread will stop.");
        }
    }  // while

    logger->Fatal("Thread stopped.");
    logger->SetLevel(LogType::Info);
}

int main() {
    FormatConfig config;
    DefaultFormatter formatter;
    formatter.SetConfig(config);

    config.SetThreadName("Main Thread");
    config.FieldName = "Test";
    config.DateFormat = "%F, %T";
    config.DateBufferSize = 64;
    config.MessageFormat = "{date} / {field} / {thread} / {logtype}: {text}";

    DefaultWriter writer;
    FileWriter logfile("output.log");

    Logger logger;
    logger.AttachFormatter(&formatter);
    logger.AttachWriter(&writer);
    logger.AttachWriter(&logfile);

    logger.Debug("This is a debug info.");
    logger.Trace("This is a trace info. {}", "What's more?");
    logger.Info("Normal information. {} + {} != {}", 1, 1, 3);
    logger.Warning("Look out!");
    logger.Error("Something {adj} happened!", "adj"_a = "bad");
    logger.Fatal("Fatal error!!!!!");

    logger.Info("Let's turn on debug output.");
    logger.SetLevel(LogType::Debug);
    logger.Debug("You can see me now!");
    logger.Trace("And me!!!");

    logger.Warning("Shutdown Debug and Trace!");
    logger.SetLevel(LogType::Info);
    logger.Debug("No......");

    logger.Info("Let's start 24 threads!!!");
    thread t[24];
    int i = 1;
    for (auto &e : t) {
        e = thread(output, &config, &logger, i);
        i++;
    }  // foreach in t

    for (auto &e : t) {
        e.join();
    }  // foreach in t

    return 0;
}  // function main
