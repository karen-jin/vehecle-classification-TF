import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:tflite/tflite.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:typed_data';
import 'package:image/image.dart' as img;

void main() => runApp(MaterialApp(
      home: DetectMain(),
      debugShowCheckedModeBanner: false,
    ));

class DetectMain extends StatefulWidget {
  @override
  _DetectMainState createState() => new _DetectMainState();
}

class _DetectMainState extends State<DetectMain> {
  File _image;
  var _recognitions;

  loadModel() async {
    Tflite.close();
    try {
      String res;
      // TODO 1. Update the model
      // Right now the model is not doing a great job classifying the
      // images and seems like it has random weights. Choose your favorite neural
      // network, train it using vehicles dataset, convert to tflite format and
      // upload it to the assets directory. Make sure to specify the correct
      // path to the model in Tflite.loadModel
      res = await Tflite.loadModel(
        model: "assets/vehicles.tflite",
        labels: "assets/labels.txt",
      );
      print(res);
    } on PlatformException {
      print("Failed to load the model");
    }
  }

  // run prediction using TFLite on given image
  Future predict(File image) async {
    var imageBytes = image.readAsBytesSync();
    img.Image oriImage = img.decodeJpg(imageBytes);
    img.Image resizedImage = img.copyResize(oriImage, width: 64, height: 32);

    // TODO 2. numResults
    // numResults is the maximum number of top guesses that model will make per one
    // prediction. Increase numResults to 3, so we could receive top 3 results
    // when we classify an image.

    var recognitions = await Tflite.runModelOnBinary(
      binary: imageToByteListFloat32(resizedImage, 64, 32, 0, 255),
      numResults: 1,
      threshold: 0.05,
    );

    // TODO 5. threshold
    // Experiment with different values of threshold. How does it affect the
    // prediction results?

    print(recognitions);

    setState(() {
      _recognitions = recognitions;
    });
  }

  // function also handles the normalization aspect
  Uint8List imageToByteListFloat32(img.Image image, int inputWidth,
      int inputHeight, double mean, double std) {
    var convertedBytes = Float32List(1 * inputWidth * inputHeight * 3);
    var buffer = Float32List.view(convertedBytes.buffer);
    int pixelIndex = 0;
    for (var i = 0; i < inputHeight; i++) {
      for (var j = 0; j < inputWidth; j++) {
        var pixel = image.getPixel(j, i);
        buffer[pixelIndex++] = (img.getRed(pixel) - mean) / std;
        buffer[pixelIndex++] = (img.getGreen(pixel) - mean) / std;
        buffer[pixelIndex++] = (img.getBlue(pixel) - mean) / std;
      }
    }
    return convertedBytes.buffer.asUint8List();
  }

  // send image to predict method selected from gallery or camera
  predictImage(File image) async {
    if (image == null) return;
    await predict(image);

    // get the width and height of selected image
    FileImage(image)
        .resolve(ImageConfiguration())
        .addListener((ImageStreamListener((ImageInfo info, bool _) {
          setState(() {
            _image = image;
          });
        })));
  }

  // select image from gallery
  selectFromGallery() async {
    var image = await ImagePicker.pickImage(source: ImageSource.gallery);
    if (image == null) return;
    setState(() {});
    predictImage(image);
  }

  // select image from camera
  selectFromCamera() async {
    var image = await ImagePicker.pickImage(source: ImageSource.camera);
    if (image == null) return;
    setState(() {});
    predictImage(image);
  }

  @override
  void initState() {
    super.initState();

    loadModel().then((val) {
      setState(() {});
    });
  }

  Widget printValue(rcg) {
    if (rcg == null) {
      return Text('',
          style: TextStyle(fontSize: 30, fontWeight: FontWeight.w700));
    } else if (rcg.isEmpty) {
      return Center(
        child: Text("Could not recognize",
            style: TextStyle(fontSize: 25, fontWeight: FontWeight.w700)),
      );
    }
    // TODO 3. More than one result
    // Since we increased our number of maximum results, let's display them all
    // on the screen. _recognitions is a list that contains results. Each result
    // object is a dictionary with the keys:
    // - index - index of the lass
    // - labels - name of the class corresponding to labels.txt
    // - confidence - probability of this result
    // Add all labels from _recognitions into recognitionsString. You may separate
    // them with a new line character
    // Note that _recognitions length may be between 0 and numResults, and not
    // nesserraly equals numResults every time.

    // TODO 4. Add confidence level
    // Along with each class show its confidence

    String recognitionsString = _recognitions[0]['label'];

    return Padding(
      padding: EdgeInsets.fromLTRB(0, 0, 0, 0),
      child: Center(
        child: Text(
          recognitionsString,
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.w700),
        ),
      ),
    );
  }

  // gets called every time the widget need to re-render or build
  @override
  Widget build(BuildContext context) {
    // get the width and height of current screen the app is running on
    Size size = MediaQuery.of(context).size;

    // initialize two variables that will represent final width and height of the segmentation
    // and image preview on screen
    double finalW = size.width;
    double finalH = finalW / 2; // 2:1 ratio

    return Scaffold(
        appBar: AppBar(
          iconTheme: IconThemeData(
            color: Colors.black, //change your color here
          ),
          title: Text(
            "Flutter Vehicles",
            style: TextStyle(color: Colors.white),
          ),
          backgroundColor: Colors.teal,
          centerTitle: true,
        ),
        body: ListView(
          children: <Widget>[
            Padding(
              padding: EdgeInsets.fromLTRB(0, 20, 0, 10),
              child: printValue(_recognitions),
            ),
            Padding(
              padding: EdgeInsets.fromLTRB(0, 0, 0, 10),
              child: _image == null
                  ? Center(
                      child: Text("Select image from camera or gallery"),
                    )
                  : Center(
                      child: Image.file(_image,
                          fit: BoxFit.fill, width: finalW, height: finalH)),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Padding(
                  padding: EdgeInsets.fromLTRB(0, 0, 20, 0),
                  child: Container(
                    height: 50,
                    width: 150,
                    color: Colors.redAccent,
                    child: FlatButton.icon(
                      onPressed: selectFromCamera,
                      icon: Icon(
                        Icons.camera_alt,
                        color: Colors.white,
                        size: 30,
                      ),
                      color: Colors.deepPurple,
                      label: Text(
                        "Camera",
                        style: TextStyle(color: Colors.white, fontSize: 20),
                      ),
                    ),
                    margin: EdgeInsets.fromLTRB(0, 20, 0, 10),
                  ),
                ),
                Container(
                  height: 50,
                  width: 150,
                  color: Colors.tealAccent,
                  child: FlatButton.icon(
                    onPressed: selectFromGallery,
                    icon: Icon(
                      Icons.file_upload,
                      color: Colors.white,
                      size: 30,
                    ),
                    color: Colors.blueAccent,
                    label: Text(
                      "Gallery",
                      style: TextStyle(color: Colors.white, fontSize: 20),
                    ),
                  ),
                  margin: EdgeInsets.fromLTRB(0, 20, 0, 10),
                ),
              ],
            ),
          ],
        ));
  }
}
