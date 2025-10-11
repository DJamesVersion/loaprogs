#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// -----------------------------------------------------------------------------
// Cross-Platform Definitions for Audio Playback Command
// -----------------------------------------------------------------------------

#ifdef _WIN32
    // Windows: Use 'start' to open the file with the default media player
    #define PLAY_COMMAND_FORMAT "start \"\" \"%s\""
    #define PLATFORM_NOTE "Using Windows 'start' command."
#elif defined(__APPLE__)
    // macOS: Use 'afplay' (built-in command line audio player)
    #define PLAY_COMMAND_FORMAT "afplay \"%s\""
    #define PLATFORM_NOTE "Using macOS 'afplay' command."
#else
    // Linux/Other POSIX: Use 'mpg123' (a common command-line MP3 player)
    // NOTE: This requires the 'mpg123' utility to be installed (e.g., 'sudo apt install mpg123').
    #define PLAY_COMMAND_FORMAT "mpg123 \"%s\""
    #define PLATFORM_NOTE "Using Linux 'mpg123' command (requires installation)."
#endif

// Define the name of the MP3 file the program looks for
#define MP3_FILE_NAME "audio.mp3"
#define MAX_COMMAND_LENGTH 512

/**
 * Main function to execute the playback command.
 */
int main() {
    char command[MAX_COMMAND_LENGTH];
    int result;

    printf("======================================\n");
    printf("      C Command-Line MP3 Player       \n");
    printf("======================================\n");

    printf("Platform Detected: %s\n", PLATFORM_NOTE);
    printf("Attempting to play: %s\n", MP3_FILE_NAME);

    // 1. Construct the system command string
    // snprintf is used for safe string formatting to prevent buffer overflows
    if (snprintf(command, MAX_COMMAND_LENGTH, PLAY_COMMAND_FORMAT, MP3_FILE_NAME) >= MAX_COMMAND_LENGTH) {
        fprintf(stderr, "Error: Command string is too long.\n");
        return 1;
    }

    printf("Executing command: %s\n", command);

    // 2. Execute the system command
    // The system() function executes the command and waits for it to complete.
    // If the external player opens in a new window, this program will continue immediately.
    result = system(command);

    // 3. Check the result of the system call
    if (result == -1) {
        fprintf(stderr, "\nERROR: Failed to execute system command (system function call failed).\n");
        return 1;
    } else if (result != 0) {
        // A non-zero result usually indicates an error with the command execution
        fprintf(stderr, "\nERROR: Playback command failed with exit code %d.\n", result);
        fprintf(stderr, "Possible causes:\n");
        fprintf(stderr, "  1. The file '%s' is missing or misspelled.\n", MP3_FILE_NAME);
        #ifdef __linux__
            fprintf(stderr, "  2. The 'mpg123' player is not installed.\n");
            fprintf(stderr, "     (Try: 'sudo apt install mpg123' or 'sudo yum install mpg123')\n");
        #else
            fprintf(stderr, "  2. The necessary system player is unavailable.\n");
        #endif
        return 1;
    }

    printf("\nPlayback command executed. Check your desktop or console for the audio player.\n");
    printf("--------------------------------------\n");

    return 0;
}

