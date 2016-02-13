# riteme-logging
A simple logger.

# Status
Current version: V0.2.0 beta

# Features
* Simple interfaces
* Easy to extend
* Multiply output
* Thread safe
* Support formatted string

# Quick start
Create a new C++ source, enter these code below:

```cpp
/**
 * main.cpp
 */

#include <rilog/Logging.hpp>  // Include this library

using namespace ri;

int main(int /* argc */, char /* *argv[] */) {
    Logger logger;

    // Set main thread's name.
    logger.GetFormatter().SetCurrentThreadName("Main Thread");

    // Output to the console.
    ConsoleWriter writer;
    logger.AttachWriter(&writer);

    // Log a info message.
    logger.Info("Hello, world!");

    return 0;
}
```

Compile & Run it:

```shell
g++ main.cpp -o main -std=c++11 -lrilog
./main
```

It would print a line of message like this:

```
[2016-02-13/13:24:47][Main Thread][INFO] Hello, world!
```

More examples see `test` directory.

# Build
First, clone this repo.  
Just make your compiler support C++11 (such as g++ >= 4.8),  
Then run `./build.py` in the root folder of this repo.  
If no errors generated, run `sudo ./install.py` to install it.
