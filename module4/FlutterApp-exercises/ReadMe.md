# Vehicle Classification Mobile App
Cross-platform application for offline vehicle image classification built with Flutter and TensorFlow Lite.

# Requirements
1. [Flutter](https://flutter.dev/docs/get-started/install)

    Flutter is Google's UI toolkit for crafting natively compiled applications for mobile, web, and desktop from a single codebase.
    Flutter apps are written in the [Dart language](https://dart.dev/guides/language). Dart is an open-source, purely object-oriented, optionally typed, and a class-based language. It's a relatively simple, modern, and highly efficient language to work with.

2. [Setup an editor](https://flutter.dev/docs/get-started/editor)
        
    The link above gives a complete installation guide on any of these:

    - *Android Studio* offers a complete, integrated IDE experience for Flutter.
    - *VS Code* is a lightweight editor with Flutter app execution and debug support.
    - *Emacs* is a lightweight editor with support for Flutter and Dart.

3. Android device or emulator

    - [Set up your Android device](https://flutter.dev/docs/get-started/install/linux#set-up-your-android-device)
    - [Set up the Android emulator](https://flutter.dev/docs/get-started/install/linux#set-up-the-android-emulator)

# To Run the App
## Android 
1. Make sure that a supported device is connected. In the terminal, run the `flutter devices` command to verify that Flutter recognizes your connected Android device

2. Run command
    ```
    fluter run
    ```

    OR

    Invoke Run/Debug action in your editor.

## iOS
`...`

# Troubleshooting
## Flutter
- To verify that the flutter command is available run
    ```
    which flutter
    ```
    If it's not you might need to update your PATH

- Run the following command to see if there are any dependencies you need to install to complete the setup (for verbose output, add the -v flag):
    ```
    flutter doctor
    ```

## App Doesn't Compile
- To install packages run
    ```
    flutter packages get
    ```

## App Doesn't Run on a Device or Crash
 - To verify that Flutter recognizes your connected Android device run 

    ```
    flutter devices
    ```

- Make sure that your device is at least 21 API version

- Might be issues with the TFLite model. Maybe it wasn't converted properly or it is not compatible with the version of the tflite package.
